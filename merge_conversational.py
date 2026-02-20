#!/usr/bin/env python3
"""
Merge conversational Q&A into main English dataset
"""

import json

def merge_datasets():
    print("📂 Loading main English dataset...")
    with open("dataset/TB_QA_DATASET_50K_ULTIMATE_V5.json", 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    print(f"✅ Loaded {len(main_data['qa_pairs']):,} existing Q&A pairs")
    
    print("\n📂 Loading conversational Q&A...")
    with open("TB_QA_CONVERSATIONAL_2K.json", 'r', encoding='utf-8') as f:
        conv_data = json.load(f)
    
    print(f"✅ Loaded {len(conv_data['qa_pairs']):,} conversational Q&A pairs")
    
    # Get the last ID from main dataset
    last_id = main_data['qa_pairs'][-1]['id']
    last_num = int(last_id.replace('Q', ''))
    
    print(f"\n🔢 Last ID in main dataset: {last_id}")
    
    # Renumber conversational Q&A to continue from main dataset
    for i, qa in enumerate(conv_data['qa_pairs'], start=1):
        new_id = f"Q{last_num + i:06d}"
        qa['id'] = new_id
    
    # Merge
    main_data['qa_pairs'].extend(conv_data['qa_pairs'])
    main_data['metadata']['count'] = len(main_data['qa_pairs'])
    main_data['metadata']['title'] += " + Conversational"
    
    print(f"\n✅ Merged dataset: {len(main_data['qa_pairs']):,} total Q&A pairs")
    
    # Save
    output_file = "dataset/TB_QA_DATASET_ENGLISH.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Saved to: {output_file}")
    print("\n✅ Merge complete!")

if __name__ == "__main__":
    merge_datasets()
