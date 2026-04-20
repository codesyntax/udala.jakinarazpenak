<div align="center">
    <h1 align="center">udala.jakinarazpenak</h1>
</div>
<div align="center">
[![PyPI](https://img.shields.io/pypi/v/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)
[![PyPI - License](https://img.shields.io/pypi/l/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)
[![PyPI - Status](https://img.shields.io/pypi/status/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)

[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/udala.jakinarazpenak)](https://pypi.org/project/udala.jakinarazpenak/)

[![CI](https://github.com/codesyntax/udala.jakinarazpenak/actions/workflows/ci.yml/badge.svg)](https://github.com/codesyntax/udala.jakinarazpenak/actions/workflows/ci.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/codesyntax/udala.jakinarazpenak)](https://github.com/codesyntax/udala.jakinarazpenak)
[![GitHub Repo stars](https://img.shields.io/github/stars/codesyntax/udala.jakinarazpenak?style=social)](https://github.com/codesyntax/udala.jakinarazpenak)

</div>

A Plone addon providing specific functionality for UdalPlone projects.

## Features

- Manages and disseminates public notifications and push alerts
- Integration with Firebase Admin
- RestAPI endpoints
- Volto-ready backend setup

## Installation

Install udala.jakinarazpenak with `pip`:

```shell
pip install udala.jakinarazpenak
```

And to create the Plone site:

```shell
make create-site
```

## Contribute

- [Issue tracker](https://github.com/codesyntax/udala.jakinarazpenak/issues)
- [Source code](https://github.com/codesyntax/udala.jakinarazpenak/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:codesyntax/udala.jakinarazpenak.git
    cd udala.jakinarazpenak
    ```

2.  Install this code base.

    ```shell
    make install
    ```

### Add features using `plonecli`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To run `plonecli` with configuration to target this package, run the following command.

```shell
make add <template_name>
```

For example, you can add a content type to your package with the following command.

```shell
make add content_type
```

## License

The project is licensed under GPLv2.
