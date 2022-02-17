import pandas as pd
import datetime as dt
from common.calc_datas import db_process, contract
import numpy as np
import math as mt

# info : df index에 month 설정이 되어있어야함


def generate_month_usage(df):
    month_usages = list()

    for name in df.columns.tolist():
        values = dict()
        kwhs = df[name]

        values['name'] = name
        for month in kwhs.index:
            values['{}'.format(month)] = int(kwhs[month])

        month_usages.append(values)

    return month_usages


def get_min_median_max(result, mean_df, x):
    mean_df = mean_df[0]
    div_x = x[3::3]

    medians = [mean_df[mean_df <= div_x[0]].median(),
               mean_df[(mean_df > div_x[0]) & (mean_df <= div_x[1])].median(),
               mean_df[(mean_df > div_x[1]) & (mean_df <= div_x[2])].median()
               ]

    target_households = list()
    target_kwhs = list()
    for medi in medians:
        idx = (mean_df - medi).abs().argmin()
        household = mean_df.index[idx]
        kwh = int(mean_df[idx])

        target_households.append(household)
        target_kwhs.append(kwh)

    target_chks = list()
    for household in target_households:
        comp = result[0]['households_bill']['comp'][0][household]
        single = result[0]['households_bill']['single'][0][household]

        for idx in comp.index:
            if comp[idx] < single[idx]:
                target_chks.append(idx)
                break

    return (target_kwhs, target_chks)


def analysis_processing_single(result, hist_df):
    in_db = dict()
    in_db['changePer'] = dict()

    # histogram data
    hist_values = hist_df.values
    bins = 9
    y, x = np.histogram(hist_values, bins=bins)

    target_kwhs, target_chks = get_min_median_max(result, hist_df, x)
    in_db['targetKwhs'] = target_kwhs
    in_db['targetChks'] = target_chks

    # 순위 구하기
    _rank = y.reshape(3, -1).sum(axis=1).argsort()
    rank = np.array([0, 0, 0])
    for idx, r in enumerate(_rank):
        rank[r] = idx
    in_db['rank'] = rank.tolist()

    x_round = x.round()
    x_str = list()

    for idx in range(len(x_round) - 1):
        x_str.append(
            "{}kWh~{}kWh".format(int(x_round[idx]), int(x_round[idx + 1] - 1))
        )

    # mean_value = hist_values[np.abs(
    #     (hist_values - hist_values.mean())).argmin()]
    # hist_mean = 0
    # hist_mean = mt.floor(bins / 2)
    # for idx in range(len(x - 1)):
    #     if (x[idx] < mean_value) and (x[idx + 1] >= mean_value):
    #         hist_mean = idx
    #         break

    x = x_str
    # hist_mean = idx

    # hist_min_sum = y[:hist_mean].sum()
    # hist_max_sum = y[hist_mean + 1:].sum()
    hist_win = "median" if rank.argmax() == 1 else \
        ("max" if rank.argmax() == 2 else "min")

    y = y.tolist()

    histogram = [{"x": _, "y": y[idx], "rank": int(
        rank[mt.floor(idx / 3)])} for idx, _ in enumerate(x)]
    in_db['histogram'] = histogram
    in_db['histWin'] = hist_win

    for main_target, sub_target, item_name in db_process:
        percentages = ["{}%".format(_) for _ in result[main_target][sub_target][contract[0]].columns.tolist(
        )]
        comp_values = result[main_target][sub_target][contract[0]].values.reshape(
            -1).tolist()
        single_values = result[main_target][sub_target][contract[1]].values.reshape(
            -1).tolist()

        item = [{
            "percentage": percentage,
            "comp": comp_values[idx],
            "single": single_values[idx]
        } for idx, percentage in enumerate(percentages)]

        change_per = int(result[1]['pos_change_per'][sub_target][0])
        in_db[item_name] = item
        in_db['changePer'][item_name] = change_per

    return in_db


def data_preprocessing(xlsx, db_processing=False):
    date_df = xlsx[3:][xlsx.columns[1:6]].copy()
    household_df = xlsx[xlsx.columns[7:]]

    date_list = [dt.datetime(
        date_df.loc[_][1],
        date_df.loc[_][2],
        date_df.loc[_][3],
        date_df.loc[_][4],
        date_df.loc[_][5]
    ) for _ in date_df.index]

    datas_df = pd.DataFrame(columns=['date'])
    datas_df['date'] = date_list

    for col in household_df:
        household_name = "{}-{}-{}".format(
            household_df[col][0],
            household_df[col][1],
            household_df[col][2]
        )
        datas_df[household_name] = household_df[col][3:].to_list()

    datas_df = datas_df.replace("-", 0)

    sum_df = pd.DataFrame(columns=['date', 'kWh', 'kW'])
    sum_df['date'] = date_list
    sum_df['kWh'] = [round(_) for _ in datas_df[datas_df.columns.difference(
        ['date'])].sum(axis=1).to_list()]
    sum_df['kW'] = (sum_df['kWh'] / 0.25).to_list()

    peak_df = pd.DataFrame(columns=['month', 'peak (kW)'])
    for month in range(1, 13):
        peak_df = peak_df.append({
            "month": str(month),
            "peak (kW)": sum_df[sum_df['date'].dt.month == month]['kW'].max()
        }, ignore_index=True)

    month_usage_df = pd.DataFrame(columns=['month'])
    month_usage_df['month'] = [_ for _ in range(1, 13)]

    for name in datas_df[datas_df.columns.difference(['date'])]:
        self_household_df = datas_df[['date', name]].copy()

        month_usage_df[name] = [
            round(
                self_household_df[self_household_df['date'].dt.month == month][name].sum())
            for month in range(1, 13)
        ]

    if db_processing:
        peaks = list()
        for idx in peak_df.index:
            month = peak_df.loc[idx]['month']
            peak = peak_df.loc[idx]['peak (kW)']
            in_dict = dict({
                "month": month,
                "peak": peak
            })

            peaks.append(in_dict)

        month_idx_m = month_usage_df.set_index("month")
        month_usages = generate_month_usage(month_idx_m)

        return (
            peak_df,
            month_usage_df,
            {
                "dpp": {
                    "peak": peaks,
                    "monthUsage": month_usages,
                }
            }
        )

    return (
        peak_df,
        month_usage_df,
        None
    )
