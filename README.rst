NotoriousPIT
============

This is the jsPsych experiment branch for the robot factory PIT task.

Quickstart
^^^^^^^^^^

The following is the minimal set of commands needed to get started:

.. code-block:: bash

    ssh <user-name>@<server-name>.princeton.edu
    git clone https://github.com/szorowi1/NotoriousPIT.git --single-branch --branch experiment
    cd NotoriousPIT
    pip install -r requirements.txt
    gunicorn -b 0.0.0.0:9000 -w 4 app:app

Wiki
^^^^

For details on how to serve the experiment, how the code is organized, and how data is stored, please see the `Wiki <https://github.com/nivlab/nivturk/wiki>`_.

Attributions
^^^^^^^^^^^^

- The original factory CSS designed by Nathan Taylor: https://codepen.io/nathantaylor/pen/MJeXmN
- The original robot CSS designed by Febby Gunawan: https://codepen.io/febby_gunawan/pen/BDjvk
