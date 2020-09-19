import ipywidgets as widgets


def make_gene_selector(symbol_series, rows=3):
    symbol_series = symbol_series.sort_values()
    return widgets.Select(options=list(zip(symbol_series.values, symbol_series.index)), rows=rows)
