# Poetry Multiproject Plugin

This is a Python `Poetry` plugin, adding the `build-project` command.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/DavidVujic/poetry-multiproject-plugin/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/DavidVujic/poetry-multiproject-plugin/tree/main)

The command will make it possible to use relative package includes.
This feature is very useful for monorepos and when sharing code between projects.

## Usage
Navigate to the project folder (where the `pyproject.toml` file is).
``` shell
poetry build-project
```

## Installation
This plugin can be installed according to the official [Poetry docs](https://python-poetry.org/docs/plugins/#using-plugins).

``` shell
poetry self add poetry-multiproject-plugin
```

## What does it do?

the `poetry build-command` will:

1. copy the actual project into a temporary folder.
2. collect relative includes - such as `include = "foo/bar", from = "../../shared"` -  and copy them into the temprary folder.
3. generate a new pyproject.toml.
4. run the `poetry build` command in the temporary folder.
5. copy the built `dist` folder (containing the wheel and sdist) into the actual project folder.
6. remove the temporary folder.


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

An suggested Monorepo structure, with the shared code extracted into a separate folder structure:

``` shell
projects/
  my_app/
    pyproject.toml (including a shared package)

  my_service/
    pyproject.toml (including other shared packages)

shared/
  my_namespace/
    my_package/
      __init__.py
      code.py

    my_other_package/
      __init__.py
      code.py
```
