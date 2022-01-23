# Poetry Multiproject Plugin

This is a `Poetry` plugin that will make it possible to build projects using custom TOML files.

This is especially useful when structuring code in a Monorepo, containing several projects.

When installed, there will be a new command available: `build-project`.

## How is it different from the "poetry build" command?
As I understand it, Poetry doesn't allow to reference code that is outside of the __project__ root.

Something like:

``` shell
packages = [{ include = "../../../my-package" }]

```

As an alternative to have a `pyproject.toml` file in a subfolder, this plugin supports a Monorepo file structure like this:

```
my-app/
   app.py

my-service/
   app.py

my-package/
   __init__.py
   my_package.py

my-other-package/
   __init__.py
   my_other_package.py

pyproject.toml
my-app.toml
my-service.toml
...
```

The different `TOML` files can include different local dependencies.
Let's say that `my-app` imports `my-package`, and `my-service` imports `my-package` only.

`my-app` and `my-service` can be built separately and include the local packages needed. By being placed at the __workspace__ root, will not cause
any issues with relative paths.


## Usage
This plugin depends on a preview of [Poetry](https://python-poetry.org/) with functionality for adding custom Plugins.
Have a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.

Install the plugin according to the [official Poetry docs](https://python-poetry.org/docs/master/cli/#plugin).

When installed, there will be a new command available: `build-project`.

This command will build your project, just like the `poetry build` command, but with a custom project TOML file.

``` shell
poetry build-project --t myproject.toml
```

(use `--t` or `--toml` to specify your custom TOML file to use)

