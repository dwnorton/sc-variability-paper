from rp2.paths import get_txburst_results_csv_path

import pandas as pd


def load_txburst_results(species, index_columns, count_type):
    csv_path = get_txburst_results_csv_path(species, index_columns, count_type)
    dtype_dict = {column: "category" for column in index_columns}

    return pd.read_csv(csv_path, dtype=dtype_dict)
