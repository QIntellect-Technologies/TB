import os
import numpy as np
import tensorflow as tf

# Handle Keras imports across different TF versions
try:
    from tf_keras.preprocessing import image
except ImportError:
    try:
        from tensorflow.keras.preprocessing import image
    except ImportError:
        import keras.preprocessing.image as image

class XRayClassifier:
    def __init__(self, model_dir: str):
        """Initialize X-Ray classifier with a SavedModel directory"""
        self.model_dir = model_dir
        self.classes = ['Normal', 'Tuberculosis']
        self.model = None
        self.concrete_fn = None
        self.input_key = None
        self.input_shape = None
        
        if os.path.exists(model_dir):
            try:
                self._load_model()
                print(f"✅ X-Ray Model loaded from {model_dir}")
                print(f"📊 Expected Input Shape: {self.input_shape}")
            except Exception as e:
                print(f"❌ Failed to load X-Ray Model: {e}")
        else:
            print(f"⚠️ X-Ray Model directory not found: {model_dir}")

    def _load_model(self):
        """Load the SavedModel with Keras 3 / TFSMLayer compatibility fallbacks"""
        try:
            # 1. Try tf_keras (Legacy Keras 2 support) - Most likely to work with existing model
            import tf_keras
            self.model = tf_keras.models.load_model(self.model_dir)
            print("✅ X-Ray Model loaded via tf_keras (Legacy)")
        except Exception as e:
            print(f"⚠️  tf_keras load failed ({e}), trying TFSMLayer...")
            try:
                # 2. Try Keras 3 TFSMLayer (Official way to load TF SavedModels in Keras 3)
                self.model = tf.keras.layers.TFSMLayer(self.model_dir, call_endpoint='serving_default')
                print("✅ X-Ray Model loaded via Keras 3 TFSMLayer")
            except Exception as e2:
                print(f"⚠️  TFSMLayer failed ({e2}), trying standard SavedModel load...")
                try:
                    # 3. Last resort: Standard tf.saved_model.load
                    self.model = tf.saved_model.load(self.model_dir)
                    self.concrete_fn = self.model.signatures.get('serving_default')
                    print("✅ X-Ray Model loaded via tf.saved_model.load")
                except Exception as e3:
                    print(f"❌ All loading methods failed. Final error: {e3}")
                    raise e3

        # Resolve Inference Function
        if hasattr(self.model, 'predict'):
            self.inference_fn = self.model.predict
        elif hasattr(self.model, 'signatures'):
            self.inference_fn = self.model.signatures.get('serving_default')
        else:
            self.inference_fn = self.model  # TFSMLayer is callable

        # Set Input Metadata (Confirmed 28x28 from local logs)
        self.input_key = "input_1"
        self.input_shape = (None, 28, 28, 3)

    def preprocess_image(self, img_path: str):
        """Resize and normalize image for model input"""
        if self.input_shape is None:
            raise RuntimeError("Model not loaded correctly")
            
        _, H, W, C = self.input_shape
        color_mode = 'rgb' if C == 3 else ('grayscale' if C == 1 else 'rgb')
        
        # Load and resize
        img = image.load_img(img_path, target_size=(H, W), color_mode=color_mode)
        arr = image.img_to_array(img)
        
        # Normalize to [0, 1]
        arr = arr.astype('float32') / 255.0
        
        # Handle grayscale conversions if necessary
        if C == 1 and arr.ndim == 3 and arr.shape[-1] == 3:
            arr = np.mean(arr, axis=-1, keepdims=True)
            
        # Add batch dimension
        return np.expand_dims(arr, axis=0)

    def predict(self, img_path: str):
        """Perform inference and return (result, confidence)"""
        if not self.model:
            return "Model Not Loaded", 0.0
            
        try:
            x = self.preprocess_image(img_path)
            
            # Using our resolved inference function
            if hasattr(self.inference_fn, '__call__'):
                # Handle dictionary input if it's a concrete function or TFSMLayer
                if not hasattr(self.model, 'predict'):
                    output = self.inference_fn(**{self.input_key: tf.convert_to_tensor(x)})
                else:
                    output = self.inference_fn(x)
            else:
                return "Inference Error: No callable found", 0.0
            
            # Extract output array
            if isinstance(output, dict):
                output = next(iter(output.values()))
            
            if hasattr(output, 'numpy'):
                y = output.numpy()
            else:
                y = output
                
            # Handle class results based on local log: (None, 28, 28, 3) -> (None, 2)
            if y.shape[-1] == 2:
                # Many models output logits or probabilities for (Normal, TB)
                probs = y[0] 
                # If these are logits, apply softmax
                if np.max(probs) > 1.0 or np.min(probs) < 0.0:
                    probs = tf.nn.softmax(y, axis=-1).numpy()[0]
                
                idx = int(np.argmax(probs))
                conf = float(np.max(probs))
                return self.classes[idx], conf
            elif y.shape[-1] == 1:
                prob_tb = float(tf.sigmoid(y)[0, 0].numpy())
                if prob_tb >= 0.5:
                    return 'Tuberculosis', prob_tb
                else:
                    return 'Normal', 1.0 - prob_tb
            else:
                raise RuntimeError(f'Unexpected output shape: {y.shape}')
                
        except Exception as e:
            print(f"❌ Inference error: {e}")
            return f"Error: {e}", 0.0
