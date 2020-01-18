[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.com/Helveg/cerebellum-scaffold.svg?token=XSpW8taq6yXK53yq1am2&branch=master)](https://travis-ci.com/Helveg/cerebellum-scaffold)
[![codecov](https://codecov.io/gh/Helveg/cerebellum-scaffold/branch/master/graph/badge.svg?token=iMOwEbV0AZ)](https://codecov.io/gh/Helveg/cerebellum-scaffold)

**Note:** The scaffold framework is still under heavy development. Please check the
**_Known Issues_** section at the bottom for important issues that fell victim to our
deadlines and will be solved at a later date.

# Scaffold: A scaffold model for the cerebellum
This package is intended to facilitate spatially, topologically and morphologically
detailed simulations of the cerebellum developed by the Department of Brain and Behavioral
Sciences at the University of Pavia.

## Installation

### Pip

This software can be installed as a Python package from PyPI through pip.

```
 pip install dbbs-scaffold
```

**Note:** *When using Anaconda, package dependency version errors might be thrown. Try
updating your package index in the Anaconda Navigator.*

## Usage

The scaffold model can be used through the command line interface or as a python package.

### Command line interface (CLI)

Run the scaffold in the command line with subcommand `compile` to compile a network
architecture.

```
scaffold --config=mouse_cerebellum.json compile -p
```

To run with different configurations, change the config argument to the relative path of a
.json config file. The `-p` flag indicates that the compiled network should be plotted
afterwards and can be omitted.

### Python package

The central object is the `scaffold.Scaffold` class. This object requires a
`scaffold.config.ScaffoldConfig` instance for its construction. To emulate the CLI
functionality you can use the `JSONConfig` class and provide the relative path to the
configuration file.

```python
from scaffold import Scaffold
from scaffold.config import JSONConfig

config = new JSONConfig(file='mouse_cerebellum.json')
scaffoldInstance = new Scaffold(config)
```

This scaffold instance can then be used to perform the subcommands available in the CLI by
calling their corresponding functions:

```python
scaffoldInstance.compile_network()
```

#### Plotting network architecture

After calling `compile_network` the scaffold instance can be passed to `plot_network` from
the `scaffold.plotting` module for plotting:

```python
from scaffold.plotting import plot_network

plot_network(scaffoldInstance)
```


# Known issues

## No configuration serialization

When modifying the config object through scripts and then saving it to file, you'll store
the original configuration file text, and you won't actually serialize the modified object

We will fix this by version 3.2
