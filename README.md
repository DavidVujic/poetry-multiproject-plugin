# Poetry Multiproject Plugin

This is a Python `Poetry` plugin, adding the `build-project` and `check-project` commands.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/DavidVujic/poetry-multiproject-plugin/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/DavidVujic/poetry-multiproject-plugin/tree/main)

[![CodeScene Code Health](https://codescene.io/projects/36629/status-badges/code-health)](https://codescene.io/projects/36629)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DavidVujic_poetry-multiproject-plugin&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DavidVujic_poetry-multiproject-plugin)

[![Download Stats](https://img.shields.io/pypi/dm/poetry-multiproject-plugin)](https://pypistats.org/packages/poetry-multiproject-plugin)


The `build-project` command will make it possible to use relative package includes.
This feature is very useful for monorepos and when sharing code between projects.

The `check-project` command is useful to check that dependencies are added properly in a project.
It uses the `MyPy` tool under the hood, and will output any errors from the static type checker.


- [Use cases](#use-cases)
- [Usage](#usage)
- [Installation](#installation)
- [What does it do?](#what-does-it-do)
- [How is it different from the "poetry build" command?](#how-is-it-different-from-the-poetry-build-command)
- [Organizing code](#organizing-code)

## Use cases

### Microservices and apps
The main use case is to support having one or more microservices or apps in a Monorepo, and share code between the services with namespaced packages.
The `build-project` command will collect the project-specific packages and build an installable artifact from it (i.e. a wheel or an sdist).

### A basic building block for the Polylith Architecture
The Multiproject plugin makes it possible to organize Python projects according to the Polylith Architecture.
The plugin is the foundation for the __Python tools for the Polylith Architecture__ - also implemented as a __Poetry__ plugin.

For more about Polylith, have a look at the [Python-specific Polylith documentation](https://davidvujic.github.io/python-polylith-docs/).

### Libraries?
Building libraries is also supported, but you will need to consider that the code will likely share the same top namespace with other libraries 
built from the same monorepo. It depends on your monorepo structure. This will likely be a problem when more than one of your libraries are installed into the same virtual environment.

Since Python libraries by default are installed in a "flat" folder structure, two libraries with the same top namespace will collide.

There is a way to solve this issue, by using the `--with-top-namespace` flag of the `build-project` command. See [usage for libraries](#usage-for-libraries).

## Usage
Navigate to the project folder (where the `pyproject.toml` file is).

Build a project:
``` shell
poetry build-project
```

Check the code used in a project:

``` shell
poetry check-project
```

Check the code, with a custom `MyPy` configuration to override the defaults:

``` shell
poetry check-project --config-file <PATH-TO-MYPY.INI-CONFIG-FILE>
```

### Usage for libraries
The `build-project` has a solution to the problem with top namespaces in libraries for __Python 3.9__ and more.
You can choose a custom namespace to be used in the build process, by using the `--with-top-namespace` flag. 

The command will organize the namespaced packages according to the custom top namespace, and more importantly, re-write the imports made in the actual source code.
The re-organizing and re-writing is performed on the relative includes.

The `build-project` command, with a custom top namespace:
```shell
poetry build-project --with-top-namespace my_namespace
```

#### The build output

###### Default(no flag)
```shell
/my_package
   __init__.py
   my_module.py
```

###### Namespace(`--with-top-namespace=my_namespace`)
```shell
my_namespace/
    /my_package
       __init__.py
       my_module.py
```

###### Namespace with path(`--with-top-namespace=my_namespace/subdir`)
```shell
my_namespace/
    /subdir
        /my_package
           __init__.py
           my_module.py
```
And will re-write the relevant module(s):

###### Default(no flag)
```python
from my_package import my_function
```

###### Namespace(`--with-top-namespace=my_namespace`)
```python
from my_namespace.my_package import my_function
```

###### Namespace with path(`--with-top-namespace=my_namespace/subdir`)
```python
from my_namespace.subdir.my_package import my_function
```

##### How is this done?
The code in this repo uses AST (Abstract Syntax Tree) parsing to modify source code.
The Python built-in `ast` module is used to parse and un-parse Python code.

## Installation
This plugin can be installed according to the official [Poetry docs](https://python-poetry.org/docs/plugins/#using-plugins).

``` shell
poetry self add poetry-multiproject-plugin
```

## What does it do?

the `poetry build-project` command will:

1. copy the actual project into a temporary folder.
2. collect relative includes - such as `include = "foo/bar", from = "../../shared"` -  and copy them into the temprary folder.
3. generate a new pyproject.toml.
4. run the `poetry build` command in the temporary folder.
5. copy the built `dist` folder (containing the wheel and sdist) into the actual project folder.
6. remove the temporary folder.


the `poetry check-project` command will:

1. copy the actual project into a temporary folder.
2. collect relative includes - such as `include = "foo/bar", from = "../../shared"` -  and copy them into the temprary folder.
3. generate a new pyproject.toml.
4. run `poetry install` in the temporary folder.
5. run `poetry run mypy` in the temporary folder.
6. remove the temporary folder.


The default setting for the underlying `MyPy` configuration is:

``` shell
--explicit-package-bases --namespace-packages --no-error-summary --no-color-output
```


## How is it different from the "poetry build" command?
Poetry does not allow package includes outside of the __project__ root.

``` shell
# Note the structure of the shared folder: namespace/package

packages = [
    { include = "my_namespace/my_package", from = "../../shared" }
    { include = "my_namespace/my_other_package", from = "../../shared" }
]
```

This plugin will allow relative package includes. You will now be able to share code between projects.

## Organizing code
An example Monorepo structure, having the shared code extracted into a separate folder structure:

``` shell
projects/
  my_app/
    pyproject.toml (including selected shared packages)

  my_service/
    pyproject.toml (including selected shared packages)

shared/
  my_namespace/
    my_package/
      __init__.py
      code.py

    my_other_package/
      __init__.py
      code.py
```

A suggested structure, using [Polylith](https://davidvujic.github.io/python-polylith-docs/workspace/):

``` shell
workspace/
  bases/
  components/
  development/
  projects/

  poetry.lock

  pyproject.toml
  workspace.toml

  README.md
```
