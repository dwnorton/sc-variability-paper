# Understanding single-cell variability via analyses of transcriptional bursting

## Python environment

A list of required packages can be found in the file `./conda/env.yml` which can be used directly to create a conda environment. For example, the following commands will create a new conda environment in the folder `./conda/env_windows` and activate it.
```
conda env create -f ./conda/env.yml -p ./conda/env_windows
conda activate ./conda/env_windows
```

If you prefer to use JupyterLab (rather than classic Jupyter) then you will also need to install `nodejs` and enable the ipywidgets extension:
```
conda install jupyterlab nodejs">=10.0.0"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
