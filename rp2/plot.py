import pandas as pd
import seaborn as sns


def scatter(*args, **kwargs):
    # Explicitly add a palette for categorical hue groups since seaborn has a problem
    # coping with numeric values in categories
    if "hue" in kwargs:
        hue_column = kwargs["hue"]
        df = kwargs["data"]
        hue_series = df[hue_column]
        if pd.api.types.is_categorical(hue_series):
            n_levels = len(hue_series.cat.categories)
            kwargs["palette"] = sns.color_palette("Set1", n_levels)

    return sns.scatterplot(*args, **kwargs)
