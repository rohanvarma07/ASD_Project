#!/usr/bin/env python3
"""
Train the ASD Detection ML Model
This script trains the advanced stacking ensemble model using your training data
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_model import ASDMLModel

def main():
    print("\n" + "="*60)
    print("ASD DETECTION MODEL - TRAINING SCRIPT")
    print("="*60)
    
    # Check if training data exists
    if not os.path.exists('train.csv'):
        print("\n❌ Error: train.csv not found!")
        print("\nPlease provide a training CSV file with the following columns:")
        print("  - ID, age, gender, ethnicity")
        print("  - A1_Score through A10_Score")
        print("  - jaundice, austim (family history)")
        print("  - Class/ASD (target variable)")
        print("\nPlace your train.csv file in the project root directory.")
        return
    
    # Initialize and train model
    model = ASDMLModel()
    
    print("\n🚀 Starting model training...")
    print("This may take several minutes...\n")
    
    try:
        results = model.train('train.csv')
        
        print("\n" + "="*60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n✅ Cross-Validation F1 Score: {results['cv_f1_score']:.4f}")
        print(f"✅ Best Threshold: {results['best_threshold']:.2f}")
        print(f"✅ Selected Features: {len(results['selected_features'])}")
        print(f"\n📁 Model saved to: models/asd_model.pkl")
        print("\n🎉 Your application is now ready to use the trained model!")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
