import os
from pathlib import Path


def make_path(*names):
    return Path(__file__).parent.parent.joinpath(*names)


def get_data_path(*names):
    return make_path("Data", *names)


def get_output_path(*names):
    return make_path("Output", *names)


def get_scripts_path(*names):
    return make_path("Scripts", *names)


def get_rp2_path(*names):
    return get_data_path("RP2", *names)


def get_model_path(model_type, *names):
    return make_path("Models", model_type, *names)


def get_txburst_results_path(*names):
    return get_model_path("txburst", *names)


class ParameterisedFilename(os.PathLike):
    def __init__(self, ext=None):
        self._filename = ""
        self._ext = f".{ext}" or ""

    def __str__(self):
        return self._filename + self._ext

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


def get_burst_model_csv_path(model_type, species, index_columns, count_type):
    filename = ParameterisedFilename(ext="csv")
    filename.append_parameter("species", species)
    filename.append_parameter("counts", count_type)
    filename.append_parameter("index", index_columns)

    return get_model_path(model_type, filename)


def get_txburst_results_csv_path(species, index_columns, count_type="umi"):
    return get_burst_model_csv_path("txburst", species, index_columns, count_type)
