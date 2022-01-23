# Poetry Multiproject Plugin

This is a `Poetry` plugin that will make it possible to build projects using custom TOML files.

This is especially useful when structuring code in a Monorepo, containing several projects.

Note: the current version (`0.1.0`) depends on a preview of [Poetry](https://python-poetry.org/) with functionality for adding custom Plugins.
Have a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.


## Usage
Install the plugin according to the [official Poetry docs](https://python-poetry.org/docs/master/cli/#plugin).

When installed, there will be a new command available: `build-project`.

This command will build your project, just like the `poetry build` command, but with a custom project TOML file.

``` shell
poetry build-project --t myproject.toml
```

(use `--t` or `--toml` to specify your custom TOML file to use)

