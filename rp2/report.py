import pandas as pd

display_name_param_map = {
    "bs_point": "Burst size",
    "bf_point": "Burst frequency",
    "log_burstiness": "Burstiness (log$_{10}$)",
    "rna_mean": "Mean mRNA count ($\\mu$)",
    "treatment": "Treatment",
}

display_name_value_map = {
    "treatment": {
        "unst": "None",
        "lps": "LPS",
        "pic": "PIC",
    }
}


def make_display_series(series):
    if series.name in display_name_value_map:
        value_map = display_name_value_map[series.name]
        series = series.map(value_map)
        series = series.astype(pd.CategoricalDtype(categories=value_map.values()))
    series = series.rename(display_name_param_map[series.name])
    return series
