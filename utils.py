import pandas as pd

def load_data():
    df = pd.read_csv("data/product_summary.csv")
    return df


def apply_filters(df, division, search, margin_threshold):
    filtered = df.copy()

    if division:
        filtered = filtered[filtered['division'].isin(division)]

    if search:
        filtered = filtered[
            filtered['product_name'].str.contains(search, case=False)
        ]

    filtered = filtered[filtered['margin'] >= margin_threshold]

    return filtered