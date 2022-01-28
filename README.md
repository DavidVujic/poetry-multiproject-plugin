# Poetry Multiproject Plugin

This is a Python `Poetry` plugin, adding commands with support for including packages outside of a project root.

This is achieved by setting the workspace (or commonly the repo) folder as the root folder.
Also, the plugin makes it possible specify a project specific `pyproject.toml` file,
useful when running commands from the workspace root.

Example usage:
running the command from the workspace root folder

``` shell
poetry build-project --t path/to/pyproject.toml
```

Optionally, run the command from the same folder as the actual project specific TOML file:

``` shell
poetry build-project
```

## Why?
Being able to specify package includes outside of a project root is especially
useful when structuring code in a Monorepo, where projects can share components.

When the plugin is installed, there is a new command available: `build-project`.

## How is it different from the "poetry build" command?
Poetry doesn't seem allow to reference code that is outside of the __project__ root.

Something like this will cause the build to fail:

``` shell
# this will fail using the default poetry build command

packages = [
    { include = "the_code_in_my_project"
    { include = "../../../my-shared-package" }]
```

By explicitly setting a workspace root, it is possible to reference outside components like this:

``` shell
packages = [
    { include = "my/project/path/the_code_in_my_project"
    { include = "shared/a-shared-package" }]
```

The project specific code is referenced with a path starting from the workspace root. The external includes can now be
referenced as if the project specific `pyproject.toml` were located at the root.


``` shell
projects/
  my-app/
    pyproject.toml (including a shared package)
    app.py

  my-service/
    pyproject.toml (including other shared packages)
    app.py

shared/
  my-package/
   __init__.py
   code.py

  my-other-package/
   __init__.py
   code.py

.workspace (a file that tells the plugin where to find the workspace root)
```

As a fallback, the plugin will look for a `pyproject.toml` or a `.git` folder to determine the workspace root.


## Using the preview of Poetry
This plugin depends on a preview of [Poetry](https://python-poetry.org/) with functionality for adding custom Plugins.
Have a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.

Install the plugin according to the [official Poetry docs](https://python-poetry.org/docs/master/cli/#plugin).

When installed, there will be a new command available: `build-project`.


## Modifying the Poetry internals
Setting the workspace root is done by altering the internal properties of the Poetry objects.
This is (naturally) a risk, an update of the Poetry tool could break the functionality of the plugin.

A long-term goal is to make a Pull Request to the Poetry repository, making this kind of functionality available
in there. If (when?) that is done, this plugin would no longer be necessary.

## What's next? Any other commands?
Starting with the `build-project` command, and ready to add more custom commands
if any of the existing ones are relevant to override when using a project specific TOML file.
