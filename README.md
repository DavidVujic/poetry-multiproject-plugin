# Poetry Multiproject Plugin

This is a Python `Poetry` plugin, adding the `build-project` command.

The command will make it possible to use relative package includes.
This feature is very useful for monorepos and when sharing code between projects.

## Usage
Navigate to the project folder (where the `pyproject.toml` file is).
``` shell
poetry build-project
```

## Installation
This plugin can be installed according to the official [Poetry docs](https://python-poetry.org/docs/plugins/#using-plugins).


## How is it different from the "poetry build" command?
Poetry does not allow package includes outside of the __project__ root.

``` shell
# Note the structure of the shared folder: namespace/package

packages = [
    { include = "my_namespace/my_package", from = "../../shared" }
    { include = "my_namespace/my_other_package", from = "../../shared" }
]
```

An example Monorepo structure:

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
