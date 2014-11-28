gocdapi
==========

.. image:: https://travis-ci.org/joaogbcravo/gocdapi.png?branch=master
        :target: https://travis-ci.org/joaogbcravo/gocdapi

About this library
-------------------

Go is a continuous delivery system - http://www.go.cd/

The goal of this python library is to be an easy interface for the Go server.

This project was inspirated in the jenkinsapi library - https://github.com/salimfadhley/jenkinsapi


This library can help you:

* Ability to list Go Agents
* Ability to enable/disable/delete a Go Agent
* Ability to list Go Pipelines Groups and their pipelines
* Ability to schedule/release lock/pause/unpause a Go Pipeline


Python versions
---------------

The project have been tested and working on 2.7


Known bugs
----------

No stable release yet. A lot of stuff to do.


Important Links
---------------

Go Continuous Delivery - http://www.go.cd/

Project source code: github: https://github.com/joaogbcravo/gocdapi


Installation
-------------

Instaling from the source
^^^^^^^^^^^^^^^^^^^^^^^^^

While there isn't a stable release hosted in PyPi, you can clone the repository and run:

.. code-block:: bash

    python setup.py install


Example
-------
gocdAPI is intended to map the objects in Go (e.g. Pipeline Groups, Pipelines, Agents) into easily managed Python objects:

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

        python setup.py test


Project Contributors
--------------------

* Joao Cravo (joaogbcravo@gmail.com)

Please do not contact these contributors directly for support questions! Use the GitHub tracker instead.


License
--------

The MIT License (MIT)
=====================

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.