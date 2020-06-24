from rp2 import check_environment, create_folder
from rp2.paths import get_output_path


class NotebookEnvironment:
    def __init__(self, intermediate_path):
        self._intermediate_path = intermediate_path

    def get_intermediate_path(self, *names):
        return self._intermediate_path.joinpath(*names)


def initialise_environment(nb_name):
    check_environment()

    output_path = get_output_path()
    create_folder(output_path)

    intermediate_path = output_path.joinpath(".intermediate", nb_name)
    create_folder(intermediate_path, create_clean=True)

    return NotebookEnvironment(intermediate_path)
