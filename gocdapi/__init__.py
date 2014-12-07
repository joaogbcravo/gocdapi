"""
About this library
==================

Go is a continuous delivery system - http://www.go.cd/
The goal of this python library is to be an easy interface for the Go server.
This project was inspirated in the jenkinsapi library - https://github.com/salimfadhley/jenkinsapi

This library can help you:

* Ability to list Go Agents
* Ability to enable/disable/delete a Go Agent
* Ability to list Go Pipelines Groups and their pipelines
* Ability to schedule/release lock/pause/unpause a Go Pipeline


Installing gocdapi
=====================

While there isn't a stable release hosted in PyPi, you can clone the repository and run:

python setup.py install


Project Authors
===============

 * Joao Cravo (joaogbcravo@gmail.com)

Current code lives on github: https://github.com/joaogbcravo/gocdapi

"""
import pkg_resources
from gocdapi import (

    # Files
    admin,
    agent,
    agents,
    custom_exceptions,
    go,
    gobase,
    pipeline,
    pipeline_group,
    pipeline_groups,
    stage
)

__all__ = [
    "admin",
    "agent",
    "agents",
    "custom_exceptions",
    "go",
    "gobase",
    "pipeline",
    "pipeline_group",
    "pipeline_groups",
    "stage"
]

__docformat__ = "epytext"
__version__ = pkg_resources.working_set.by_key['gocdapi'].version
