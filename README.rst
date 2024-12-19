UpTainer
========
.. image:: https://img.shields.io/github/license/asbarbati/uptainer
   :alt: GitHub License
.. image:: https://img.shields.io/codecov/c/gh/asbarbati/uptainer
   :alt: Codecov

.. image:: https://readthedocs.org/projects/uptainer/badge/?version=latest
        :target: https://uptainer.readthedocs.io/
        :alt: Documentation Status

Uptainer is a Python CLI that automates tool updates, ensuring consistency and reliability in your GitOps-driven infrastructure.

The tool offers a straightforward interface for specifying the repository from which to read and write, as well as the regular expression to constrain version increments. The tool will then handle the remaining automation tasks.

What are the ideal applications for this tool?
----------------------------------------------
In any scenario where you employ a continuous delivery tools (like `ArgoCD <https://github.com/argoproj/argo-cd>`_, `Flux <https://github.com/fluxcd/flux2>`_, ecc) to deploy the applications you manage.

Features
--------
* Built-in Integration with DockerHub.
* Built-in integration with Github Container Hub (Ghcr.io).
* Restricts updates based on a specific regular expression.
* Use a specific ssh key for pull/push the git commit.
* You can also specify multiple branches with distinct conditions.
* Output log in json format.

More information: `ReadTheDocs <https://uptainer.readthedocs.io>`_

Quick Start
-----------
1. Create a new virtualenv using `python3 -m venv venv`
2. Load it using `. ./.venv/bin/activate`
3. Install the pkg using `pip install uptainer`
4. Copy the sample configuration into config.yaml `cp config.sample.yaml config.yaml`
5. Edit the configuration in the config file as your environment.
6. Run it using `python3 -m uptainer.cli --config-file config.yaml`

Contributing
------------
Contributions, issues and feature requests are welcome.

Feel free to check `Issue <https://github.com/asbarbati/uptainer/issues>`_ page if you want to contribute.

Check the `Contributing Guide <https://github.com/asbarbati/uptainer/blob/develop/CONTRIBUTING.rst>`_.

License
--------
Copyright © Alessandro Sbarbati.

This project is GNU GENERAL PUBLIC LICENSE v3 licensed.
