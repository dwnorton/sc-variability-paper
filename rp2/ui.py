import ipywidgets as widgets
from matplotlib import pyplot as plt


def make_gene_selector(symbol_series, rows=3):
    symbol_series = symbol_series.sort_values()
    return widgets.Select(options=list(zip(symbol_series.values, symbol_series.index)), rows=rows)


def zero_axes_origin(ax=None):
    ax = ax or plt.gca()
    x_max = ax.get_xlim()[1]
    ax.set_xlim(left=-(x_max / 20))
    y_max = ax.get_xlim()[1]
    ax.set_ylim(bottom=-(y_max / 20))
