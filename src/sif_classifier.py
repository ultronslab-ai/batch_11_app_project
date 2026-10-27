import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

HIGH_RISK_TRIGGER_PHRASES = [
    'harness', 'life line', 'height', 'scaffolding', 'hot work', 'gas leak',
    'confined space', 'oxygen', 'sling', 'crane lift', 'isolation', 'loto',
    'excavation', 'trench', '11kv', 'high voltage', 'pinch zone', 'interlock',
    'bypassed', 'suspended load', 'toxic gas', 'overturn', 'fall'
]

def compute_risk_score(sif_prob_pct: float, lsr_tags: list, factors: list) -> dict:
    """Compute normalized 1 to 10 HSE Risk Score and Severity Level."""
    # Base score (0.0 to 10.0)
    base_score = (sif_prob_pct / 100.0) * 8.5
    
    # LSR multiplier boost (+0.5 per extra life saving rule)
    lsr_count = len([t for t in lsr_tags if t not in ['None', 'General Operations']])
    lsr_boost = min(1.5, lsr_count * 0.5) if lsr_count > 0 else 0.0
    
    # Critical barrier boost
    critical_kws = ['harness', 'isolation', '11kv', 'oxygen', 'bypassed', 'trench', 'suspended load']
    factor_boost = 0.5 if any(kw in str(factors).lower() for kw in critical_kws) else 0.0
    
    raw_score = base_score + lsr_boost + factor_boost
    final_score = round(min(10.0, max(1.0, raw_score)), 1)
    
    if final_score >= 8.0:
        level = "CRITICAL RISK"
        color = "#FF0055"
        badge_class = "risk-critical"
    elif final_score >= 6.0:
        level = "HIGH RISK"
        color = "#FF5722"
        badge_class = "risk-high"
    elif final_score >= 3.5:
        level = "MEDIUM RISK"
        color = "#FFC107"
        badge_class = "risk-medium"
    else:
        level = "LOW RISK"
        color = "#238636"
        badge_class = "risk-low"

    return {
        "risk_score": final_score,
        "risk_level": level,
        "risk_color": color,
        "badge_class": badge_class
    }

class SIFClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=1000)),
            ('clf', LogisticRegression(C=1.5, max_iter=200, class_weight='balanced'))
        ])
        self.is_fitted = False
        self.feature_names = []

    def fit(self, texts: list, labels: list):
        """Fit TF-IDF + Logistic Regression model."""
        self.pipeline.fit(texts, labels)
        self.is_fitted = True
        self.feature_names = self.pipeline.named_steps['tfidf'].get_feature_names_out()
        return self

    def predict_one(self, text: str, lsr_tags: list = None) -> dict:
        """Predict SIF probability, 1-10 Risk Score, label, confidence, and explainability for single text."""
        text_clean = str(text).lower().strip()
        
        if not self.is_fitted:
            prob = self._heuristic_score(text_clean)
        else:
            probs = self.pipeline.predict_proba([text_clean])[0]
            prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            
            trigger_count = sum(1 for phrase in HIGH_RISK_TRIGGER_PHRASES if phrase in text_clean)
            if trigger_count >= 2:
                prob = max(prob, 0.85)
            elif trigger_count == 1:
                prob = max(prob, 0.65)

        sif_label = "SIF-Potential" if prob >= 0.50 else "Non-SIF"
        confidence = float(np.round(max(prob, 1.0 - prob), 4))
        
        contributing_factors = self._extract_explainability_factors(text_clean)
        explanation = self._build_explanation_summary(sif_label, prob, contributing_factors)

        prob_pct = round(prob * 100, 1)
        risk_info = compute_risk_score(prob_pct, lsr_tags or [], contributing_factors)

        return {
            "sif_probability": prob_pct,
            "sif_label": sif_label,
            "confidence_score": round(confidence * 100, 1),
            "contributing_factors": contributing_factors,
            "explanation": explanation,
            "risk_score": risk_info["risk_score"],
            "risk_level": risk_info["risk_level"],
            "risk_color": risk_info["risk_color"],
            "badge_class": risk_info["badge_class"]
        }

    def predict_batch(self, df: pd.DataFrame, text_col: str = 'report_text') -> pd.DataFrame:
        """Score dataframe and return enhanced columns including 1-10 Risk Score."""
        res_df = df.copy()
        probs = []
        labels = []
        factors_list = []
        explanations = []
        risk_scores = []
        risk_levels = []
        risk_colors = []

        for idx, row in res_df.iterrows():
            txt = row[text_col]
            lsr_list = str(row.get('ground_truth_lsr', '')).split(';')
            res = self.predict_one(txt, lsr_list)
            probs.append(res['sif_probability'])
            labels.append(res['sif_label'])
            factors_list.append(", ".join(res['contributing_factors']))
            explanations.append(res['explanation'])
            risk_scores.append(res['risk_score'])
            risk_levels.append(res['risk_level'])
            risk_colors.append(res['risk_color'])

        res_df['sif_probability'] = probs
        res_df['sif_label'] = labels
        res_df['contributing_factors'] = factors_list
        res_df['explanation'] = explanations
        res_df['risk_score'] = risk_scores
        res_df['risk_level'] = risk_levels
        res_df['risk_color'] = risk_colors

        # Sort by highest Risk Score first
        res_df = res_df.sort_values(by='risk_score', ascending=False).reset_index(drop=True)
        return res_df

    def _heuristic_score(self, text: str) -> float:
        matches = sum(1 for phrase in HIGH_RISK_TRIGGER_PHRASES if phrase in text)
        if matches >= 2:
            return 0.88
        elif matches == 1:
            return 0.62
        return 0.20

    def _extract_explainability_factors(self, text: str) -> list:
        factors = []
        for phrase in HIGH_RISK_TRIGGER_PHRASES:
            if phrase in text:
                factors.append(phrase)
        
        # If model is fitted, also check top weighted tfidf tokens
        if self.is_fitted:
            tfidf = self.pipeline.named_steps['tfidf']
            clf = self.pipeline.named_steps['clf']
            vec = tfidf.transform([text]).toarray()[0]
            coefs = clf.coef_[0]
            
            # Find active features with positive SIF weights
            active_indices = np.where(vec > 0)[0]
            top_active = sorted(active_indices, key=lambda idx: coefs[idx], reverse=True)[:5]
            for idx in top_active:
                w = coefs[idx]
                if w > 0:
                    feat = self.feature_names[idx]
                    if feat not in factors:
                        factors.append(feat)

        return factors[:6] if factors else ["Routine operational activity"]

    def _build_explanation_summary(self, label: str, prob: float, factors: list) -> str:
        if label == "SIF-Potential":
            factor_str = ", ".join([f"'{f}'" for f in factors])
            return f"Flagged as HIGH SIF-Potential ({prob*100:.1f}%) due to dangerous precursors: {factor_str}. Immediate HSE intervention recommended."
        else:
            return f"Classified as Low/Non-SIF Potential ({prob*100:.1f}%). No life-threatening precursors or severe barrier failures identified."
