from rp2 import paths
from rp2.paths import get_txburst_results_csv_path

import pandas as pd


def load_txburst_results(species, index_columns, count_type):
    csv_path = get_txburst_results_csv_path(species, index_columns, count_type)
    dtype_dict = {column: "category" for column in index_columns}

    return pd.read_csv(csv_path, dtype=dtype_dict)


def load_and_recalculate_txburst_results(species, condition_columns, count_type, bursty=False):
    df = load_txburst_results(species, condition_columns, count_type)
    df = df.loc[df.keep]

    df["bf_point"] = df.k_on if bursty else (df.k_on * df.k_off) / (df.k_on + df.k_off)
    df["bs_point"] = df.k_syn / df.k_off

    return df.drop(columns=["bf_lower", "bf_upper", "bs_lower", "bs_upper", "keep"])


def load_rp2_analysis_genes():
    return pd.read_csv(paths.get_rp2_path("analysis_genes.csv"), index_col=0)
