# Sudoku

This repository implements a Sudoku solver using Pyomo, a Python-based optimization 
library. The model is built using an abstract formulation where the grid size is flexible 
(default 9x9). The model defines all the necessary sets, parameters, variables,
constraints and the objective function to solve this problem.

Find [here](modeling.pdf) the model expressed mathematically.

## Installation

- Base enviornment: You should have installed Python and pip.
- Miniconda (or Conda): It provides the most straightforward installation of the solver, already compiled. Check out [this](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#term-Miniconda) page.


## Development tools

- Type checking with flake8:
```bash
$ flake8 --max-line-length=89
```

## Running
```bash
$ python main.py
```

## Code structure
- `main.py`: Main execution file. It orchestrates the execution.
- `model.py`: Model definition and construction.
- `solver.py`: Defines the solver and its functions.
- `concrete_model_dump.txt`: Internal structure of the model (for debugging)
- `conda-env.yml`: Environment for Conda/Miniconda.
- `requirements.txt`: Requirements of the project.

## Attributions
- Base of the code and ideas extracted from _Josep's blog_ [here](https://johomo.hashnode.dev/solve-your-first-problem-with-mathematical-programming).
- Definition of the rooks problem extracted from [here](https://mathworld.wolfram.com/RooksProblem.html).
