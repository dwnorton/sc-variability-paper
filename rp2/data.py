from rp2.paths import get_txburst_results_csv_path

import pandas as pd


def load_txburst_results(species, index_columns, count_type):
    csv_path = get_txburst_results_csv_path(species, index_columns, count_type)
    dtype_dict = {column: "category" for column in index_columns}

    return pd.read_csv(csv_path, dtype=dtype_dict)


def load_modified_txburst_results(species, condition_columns, count_type, two_alleles=False):
    df = load_txburst_results(species, condition_columns, count_type)
    df = df.loc[df.bf_point.notna() & df.bs_point.notna()]

    df["bf_point"] = (2 * df.k_on * df.k_off) / (df.k_on + df.k_off) if two_alleles else df.k_on
    df["bs_point"] = df.k_syn / df.k_off

    return df.drop(columns=["bf_lower", "bf_upper", "bs_lower", "bs_upper", "keep"])
