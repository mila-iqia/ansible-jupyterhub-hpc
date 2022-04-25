# Jupyter IDRIS Slurm Spawner

This project contains custom SLURM spawner customized for Jean Zay platform

## Installation

The package can be installed using
```
pip install git+https://gitlab.com/i2461/jupyter/jupyter-jean-zay-slurm-spawner.git
```

## Testing

A basic functional test is included in the package and it can tested using
```
conda create -n <myenv> python=<pyver>
conda activate <myenv>
git clone https://gitlab.com/i2461/jupyter/jupyter-jean-zay-slurm-spawner.git
cd jupyter-jean-zay-slurm-spawner/
pip install -r requirements-test.txt
pytest --verbose tests/
```

## Usage

This spawner can be used in the Jupyterhub by using the following configuration
```
import jeanzay_spawner
c.JupyterHub.spawner_class = 'jeanzay_spawner.JeanZaySlurmSpawner'
```