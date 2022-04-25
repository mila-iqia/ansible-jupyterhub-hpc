# Custom Slurm Spawner

This project contains customizable SLURM spawner.


## Usage

This spawner can be used in the Jupyterhub by using the following configuration
```
import custom_slurm_spawner
c.JupyterHub.spawner_class = 'custom_slurm_spawner.CustomSlurmSpawner'
```