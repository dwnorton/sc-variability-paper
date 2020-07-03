import os
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


class ParameterisedFilename(os.PathLike):
    def __init__(self, ext=None):
        self._filename = ""
        self._ext = f".{ext}" or ""

    def __fspath__(self):
        return self._filename + self._ext

    def append(self, text):
        if self._filename:
            self._filename += "_"
        self._filename += text


def get_txburst_results_csv_path(species, combined_replicates=False):
    filename = ParameterisedFilename(ext="csv")
    filename.append(species)
    filename.append("umi")
    if combined_replicates:
        filename.append("combined_replicates")

    return get_txburst_results_path(filename)
