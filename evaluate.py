import os
import sys

# Ensure project root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

from src.ingestion import validate_and_clean_df
from src.sif_classifier import SIFClassifier
from src.lsr_tagger import LSRTagger

def run_evaluation():
    print("=" * 65)
    print("SIH26165: SIF Precursor Classifier & LSR Model Evaluation")
    print("=" * 65)

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_sif_reports.csv')
    if not os.path.exists(data_path):
        print(f"Error: Sample data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    df = validate_and_clean_df(df)

    # Train / Test split
    X = df['report_text']
    y = df['ground_truth_sif']

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    print(f"\n[1] Dataset Summary:")
    print(f"    - Total Reports: {len(df)}")
    print(f"    - Train Samples: {len(X_train)} | Validation Samples: {len(X_val)}")
    print(f"    - SIF Class Balance: {dict(y.value_counts())}")

    # Train classifier
    classifier = SIFClassifier()
    classifier.fit(list(X_train), list(y_train))

    # Evaluate SIF Classification
    y_pred_probs = []
    y_preds = []

    for text in X_val:
        res = classifier.predict_one(text)
        prob = res['sif_probability'] / 100.0
        y_pred_probs.append(prob)
        y_preds.append(1 if res['sif_label'] == 'SIF-Potential' else 0)

    print("\n[2] SIF Classification Performance Metrics (Validation Split):")
    report = classification_report(y_val, y_preds, target_names=['Non-SIF (0)', 'SIF-Potential (1)'], output_dict=False)
    print(report)

    try:
        auc = roc_auc_score(y_val, y_pred_probs)
        print(f"    -> ROC-AUC Score: {auc:.4f}")
    except Exception as e:
        print(f"    -> ROC-AUC Score: N/A ({e})")

    cm = confusion_matrix(y_val, y_preds)
    print(f"\n[3] Confusion Matrix:")
    print(f"    [[TN: {cm[0][0]}, FP: {cm[0][1]}],")
    print(f"     [FN: {cm[1][0]}, TP: {cm[1][1]}]]")

    # Evaluate LSR Multi-label Tagger
    tagger = LSRTagger()
    print("\n[4] IOGP Life-Saving Rules Multi-Label Tagging Sample:")
    sample_eval_texts = X_val.iloc[:3]
    for idx, sample in enumerate(sample_eval_texts, 1):
        tags = tagger.tag_text(sample)
        print(f"    Sample {idx}: '{sample[:70]}...'")
        print(f"    Tagged Rules: {tags}\n")

    print("=" * 65)
    print("Evaluation Complete. All models ready for Hackathon Demo!")
    print("=" * 65)

if __name__ == '__main__':
    run_evaluation()
