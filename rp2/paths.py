from pathlib import Path

data_path = Path(__file__).parent.parent.joinpath("Data")
output_path = Path(__file__).parent.parent.joinpath("Output")
scripts_path = Path(__file__).parent.parent.joinpath("Scripts")


def get_data_path(*names):
    return data_path.joinpath(*names)


def get_output_path(*names):
    return output_path.joinpath(*names)


def get_scripts_path(*names):
    return scripts_path.joinpath(*names)


def get_txburst_results_path(*names):
    return get_output_path("txburst", *names)


def get_txburst_results_csv_path(species, combined_replicates=False):
    suffix = "_combined_replicates" if combined_replicates else ""
    return get_txburst_results_path(f"{species}_responsive_genes{suffix}.csv")
