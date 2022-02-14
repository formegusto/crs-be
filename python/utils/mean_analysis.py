import pandas as pd
from utils import *


def mean_analysis(month_usage_df, peak_df, min_per, max_per, db_processing=False):
    analysis_targets = month_usage_df.set_index("month").copy()
    hist_df = pd.DataFrame(analysis_targets.mean(axis=0).round())
    mean_df = hist_df.copy().T

    mean_df['month'] = 1

    bc_result = bill_calc(mean_df, peak_df, min_per, max_per)
    na_result = normal_analysis(bc_result)

    if db_processing:
        mean_analysis = analysis_processing_single(
            (bc_result, na_result), hist_df)
        reco_percentage = mean_analysis['changePer']['positiveCount']
        return {
            "kwh": bc_result['information'][0]['sum'],
            "recoPercentage": reco_percentage,
            "meanAnalysis": mean_analysis
        }

    return bc_result, na_result
