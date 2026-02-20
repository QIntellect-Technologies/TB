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
        """Load the SavedModel with multiple fallbacks for compatibility"""
        try:
            # Try standard SavedModel load first
            self.model = tf.saved_model.load(self.model_dir)
            self.concrete_fn = self.model.signatures.get('serving_default')
        except Exception as e:
            print(f"⚠️  tf.saved_model.load failed ({e}), trying keras fallback...")
            try:
                # Try Keras load_model as fallback (often handles version mismatches better)
                self.model = tf.keras.models.load_model(self.model_dir)
                self.concrete_fn = self.model.signatures.get('serving_default')
            except Exception as e2:
                print(f"❌ Keras fallback also failed: {e2}")
                raise e

        if self.concrete_fn is None:
            # If load_model worked but didn't provide signatures, it might be a Keras object
            if hasattr(self.model, 'predict'):
                # We can use the model directly
                self.input_shape = self.model.input_shape if hasattr(self.model, 'input_shape') else (None, 224, 224, 3)
                print("✅ Using Keras model.predict directly")
                return
            raise RuntimeError('SavedModel has no serving_default signature and no model.predict')
        
        # Extract input key and shape
        try:
            input_info = self.concrete_fn.structured_input_signature[1]
            self.input_key = list(input_info.keys())[0]
            self.input_shape = tuple(list(input_info.values())[0].shape.as_list())
        except Exception as e:
            print(f"⚠️  Signature extraction failed: {e}. Using defaults.")
            self.input_key = "input_1" # Common default
            self.input_shape = (None, 224, 224, 3)

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
            tensor_x = tf.convert_to_tensor(x)
            
            # Run inference
            output = self.concrete_fn(**{self.input_key: tensor_x})
            
            # Handle dictionary output
            if isinstance(output, dict):
                output = next(iter(output.values()))
            
            # Get numpy array
            if hasattr(output, 'numpy'):
                y = output.numpy()
            else:
                y = output # Fallback
                
            # Interpret results
            if y.shape[-1] == 2:
                # Softmax case
                probs = tf.nn.softmax(y, axis=-1).numpy()[0]
                idx = int(np.argmax(probs))
                conf = float(np.max(probs))
                return self.classes[idx], conf
            elif y.shape[-1] == 1:
                # Sigmoid case
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
