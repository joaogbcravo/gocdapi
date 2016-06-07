gocdapi
==========

.. image:: https://badge.fury.io/py/gocdapi.png
    :target: http://badge.fury.io/py/gocdapi

.. image:: https://travis-ci.org/joaogbcravo/gocdapi.png?branch=master
        :target: https://travis-ci.org/joaogbcravo/gocdapi

About this library
-------------------

Go is a continuous delivery system - http://www.go.cd/

The goal of this python library is to be an easy interface for the Go server.

This project was inspirated in the jenkinsapi library - https://github.com/salimfadhley/jenkinsapi


This library can help you:

* to list Go Agents
* to enable/disable/delete a Go Agent
* to see a job run history of an Go Agent
* to list Go Pipelines Groups and their Pipelines
* to schedule/release lock/pause/unpause a Go Pipeline
* to create and delete Go Pipelines from a XML config or delete Go Pipelines
* to create and delete Go Pipelines Groups
* to cancel a Go Stage run or see it's history


Python versions
---------------

The project have been tested and working on 2.7


Known bugs
----------

Currently compatible with Go version 14.3.0-1186.
No know bugs at the moment.


Important Links
---------------

Go Continuous Delivery - http://www.go.cd/

Project source code: github: https://github.com/joaogbcravo/gocdapi


Installation
-------------

Using Pip
^^^^^^^^^

Run the command:

.. code-block:: bash

    pip install gocdapi


Instaling from the source
^^^^^^^^^^^^^^^^^^^^^^^^^

You can clone the repository and install:

.. code-block:: bash

    git clone https://github.com/joaogbcravo/gocdapi.git
    python setup.py install


Example
-------
gocdAPI is intended to map the objects in Go (e.g. Pipeline Groups, Pipelines, Agents) into easily managed Python
objects:

.. code-block:: python

        >>> from gocdapi.go import Go
        >>> go_server =  Go("http://localhost:8153/")
        >>>
        >>> for uuid, agent in go_server.agents:
        ...     print uuid, " - ", agent
        ...
        a8b7c2b4-3986-476a-a797-abb3a065587e  -  Agent @ http://localhost:8153/
        >>>
        >>> agent = go_server.agents["a8b7c2b4-3986-476a-a797-abb3a065587e"]
        >>> agent.enable()
        >>> print agent.status
        Idle
        >>>
        >>> agent.disable()
        >>> print agent.status
        Disabled
        >>>
        >>> for name, pipeline_group in go_server.pipeline_groups:
        ...     print name, " - ", pipeline_group
        ...
        Development  -  Pipeline @ http://localhost:8153/
        >>>
        >>> pipeline_group = go_server.pipeline_groups["Development"]
        >>> for name, pipeline in pipeline_group:
        ...     print name, " - ", pipeline
        ...
        Web_Services_QA  -  Pipeline @ http://localhost:8153/
        Deploy_Web_Services  -  Pipeline @ http://localhost:8153/
        >>>


Testing
-------

After the installation of the test dependencies on your system, run the command:

.. code-block:: bash

        python setup.py nosetests

Nose need a Go Server and Agent to run, so when you execute nosetests it will start a new Go Server and Agent, and it
will shutdown them after all the test run. If you haven't the executable in the gocdapi_tests/systests folder it will
download them. This process can be slow, so you can start by yourself a Go Server and Agent and run nosetests in the
following way:

.. code-block:: bash

        python nosetests -s --nologcapture --tc=static_instances:true

To make a source code analysis, you can run pep8 and pylint:

.. code-block:: bash

        pep8 --ignore=E501 gocdapi/*.py
        pylint --rcfile=pylintrc gocdapi/*.py


Project Contributors
--------------------

* Joao Cravo (joaogbcravo@gmail.com)
* Joao Vale (jpvale@gmail.com)

Please do not contact these contributors directly for support questions! Use the GitHub tracker instead.


License
--------

The MIT License (MIT)
=====================

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
