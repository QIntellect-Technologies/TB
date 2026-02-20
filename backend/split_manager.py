import os
import glob

def split_file(filepath, chunk_size_mb=45):
    """Split a large file into smaller chunks for GitHub."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
    
    file_size = os.path.getsize(filepath)
    chunk_size = chunk_size_mb * 1024 * 1024
    
    if file_size <= chunk_size:
        print(f"File {filepath} is small enough ({file_size/1024/1024:.1f}MB). No splitting needed.")
        return []

    print(f"Splitting {filepath} ({file_size/1024/1024:.1f}MB) into {chunk_size_mb}MB chunks...")
    
    chunks = []
    with open(filepath, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            chunk_name = f"{filepath}.part{part_num}"
            with open(chunk_name, 'wb') as chunk_file:
                chunk_file.write(chunk)
            
            chunks.append(chunk_name)
            part_num += 1
            
    print(f"✅ Created {len(chunks)} chunks for {filepath}")
    return chunks

def join_files(original_path):
    """Reassemble chunks into the original file."""
    chunk_pattern = f"{original_path}.part*"
    chunks = sorted(glob.glob(chunk_pattern), key=lambda x: int(x.split('.part')[-1]))
    
    if not chunks:
        return False
    
    # If the original file already exists and has size > 0, we don't need to join
    # but on Railway, if LFS failed, the file might exist but be a pointer file (size < 1KB)
    if os.path.exists(original_path) and os.path.getsize(original_path) > 1024 * 1024:
        return True

    print(f"Reassembling {original_path} from {len(chunks)} chunks...")
    with open(original_path, 'wb') as output_file:
        for chunk_path in chunks:
            with open(chunk_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())
                
    print(f"✅ Reassembled {original_path}")
    return True

if __name__ == "__main__":
    # Files to split locally before pushing
    files_to_split = [
        "backend/vector_db_faiss/english.index",
        "backend/vector_db_faiss/urdu.index",
        "backend/tb_expert.db",
        "backend/vector_db_faiss/urdu_metadata.pkl"
    ]
    
    for f in files_to_split:
        if os.path.exists(f):
            split_file(f)
