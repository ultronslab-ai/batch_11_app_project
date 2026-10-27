import pandas as pd
import numpy as np

def compute_overall_metrics(df: pd.DataFrame) -> dict:
    """Compute high-level HSE dashboard KPIs."""
    total_reports = len(df)
    if total_reports == 0:
        return {
            "total_reports": 0,
            "sif_count": 0,
            "sif_rate": 0.0,
            "top_lsr": "N/A",
            "top_risky_site": "N/A",
            "avg_risk_score": 0.0
        }

    sif_df = df[df['sif_label'] == 'SIF-Potential']
    sif_count = len(sif_df)
    sif_rate = round((sif_count / total_reports) * 100, 1)

    # Average Risk Score (1-10 scale)
    avg_risk_score = round(df['risk_score'].mean(), 1) if 'risk_score' in df.columns else 0.0

    # Top Life-Saving Rule
    lsr_series = df['lsr_tags'].str.split('; ').explode()
    lsr_series = lsr_series[lsr_series != 'None']
    top_lsr = lsr_series.mode()[0] if not lsr_series.empty else "None"

    # Top Risky Site
    site_sif = df.groupby('site')['risk_score'].mean() if 'risk_score' in df.columns else df.groupby('site')['sif_probability'].mean()
    top_risky_site = site_sif.idxmax() if not site_sif.empty else "N/A"

    return {
        "total_reports": total_reports,
        "sif_count": sif_count,
        "sif_rate": sif_rate,
        "top_lsr": top_lsr,
        "top_risky_site": top_risky_site,
        "avg_risk_score": avg_risk_score
    }

def get_site_risk_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """Rank sites by 1-10 Risk Score and SIF-precursor density."""
    if 'risk_score' not in df.columns:
        df['risk_score'] = (df['sif_probability'] / 10.0).round(1)

    group = df.groupby('site').agg(
        total_reports=('report_id', 'count'),
        sif_potential_reports=('sif_label', lambda x: (x == 'SIF-Potential').sum()),
        avg_risk_score=('risk_score', 'mean'),
        avg_sif_probability=('sif_probability', 'mean')
    ).reset_index()

    group['avg_risk_score (1-10)'] = group['avg_risk_score'].round(1)
    group['sif_precursor_density_pct'] = (group['sif_potential_reports'] / group['total_reports'] * 100).round(1)
    group['avg_sif_probability'] = group['avg_sif_probability'].round(1)
    
    group = group.drop(columns=['avg_risk_score'])
    group = group.sort_values(by=['avg_risk_score (1-10)', 'sif_precursor_density_pct'], ascending=False).reset_index(drop=True)
    group.index = group.index + 1
    group.index.name = 'Risk Rank'
    return group

def get_activity_risk_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """Rank activities by 1-10 Risk Score and SIF-precursor density."""
    if 'risk_score' not in df.columns:
        df['risk_score'] = (df['sif_probability'] / 10.0).round(1)

    group = df.groupby('activity').agg(
        total_reports=('report_id', 'count'),
        sif_potential_reports=('sif_label', lambda x: (x == 'SIF-Potential').sum()),
        avg_risk_score=('risk_score', 'mean'),
        avg_sif_probability=('sif_probability', 'mean')
    ).reset_index()

    group['avg_risk_score (1-10)'] = group['avg_risk_score'].round(1)
    group['sif_precursor_density_pct'] = (group['sif_potential_reports'] / group['total_reports'] * 100).round(1)
    group['avg_sif_probability'] = group['avg_sif_probability'].round(1)
    
    group = group.drop(columns=['avg_risk_score'])
    group = group.sort_values(by=['avg_risk_score (1-10)', 'sif_precursor_density_pct'], ascending=False).reset_index(drop=True)
    group.index = group.index + 1
    group.index.name = 'Risk Rank'
    return group

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate reports by month and SIF classification."""
    df_temp = df.copy()
    df_temp['month'] = pd.to_datetime(df_temp['date']).dt.strftime('%Y-%m')
    trend = df_temp.groupby(['month', 'sif_label'])['report_id'].count().unstack(fill_value=0).reset_index()
    if 'SIF-Potential' not in trend.columns:
        trend['SIF-Potential'] = 0
    if 'Non-SIF' not in trend.columns:
        trend['Non-SIF'] = 0
    return trend

def get_heatmap_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Generate Site vs Activity SIF precursor density heatmap matrix."""
    pivot = pd.pivot_table(
        df,
        values='sif_probability',
        index='site',
        columns='activity',
        aggfunc='mean',
        fill_value=0
    ).round(1)
    return pivot
