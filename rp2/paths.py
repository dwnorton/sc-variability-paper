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
        assert("-" not in text)
        if self._filename:
            self._filename += "-"
        self._filename += text
        return self

    def append_parameter(self, name, value):
        if isinstance(value, (list, tuple)):
            value = "+".join(value)
        assert("=" not in name)
        assert("=" not in value)
        self.append(f"{name}={value}")
        return self


def get_txburst_results_csv_path(species, index_columns):
    filename = ParameterisedFilename(ext="csv")
    filename.append_parameter("species", species)
    filename.append_parameter("counts", "umi")
    filename.append_parameter("index", index_columns)

    return get_txburst_results_path(filename)
