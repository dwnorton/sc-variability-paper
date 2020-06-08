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
