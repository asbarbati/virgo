=====
Usage
=====

CLI Tool
--------

0. (OPTIONAL) Create and activate a Python virtual environment to isolate project dependencies from the system's global libraries.

.. code-block:: bash

    python3 -m venv .venv
    . ./.venv/bin/activate

1. Install the package using:

.. code-block:: bash

    pip install uptainer


2. Download the latest config sample from Github

.. code-block:: bash

    wget "https://raw.githubusercontent.com/asbarbati/uptainer/refs/heads/develop/config.sample.yaml"

3. Edit the config based your scenarios follow the :doc:`configuration guide <config>`.

4. Export the environment variable named "GITHUB_API_TOKEN" (:doc:`How to create the tokens </create_token>`)

.. code-block:: bash

    export GITHUB_API_TOKEN="ghp_...."

5. Run it using:

.. code-block:: bash

    uptainer --config-file <path of your config yml>

6. Verify the results on the logs.


Helm Chart
----------

Work in progress
