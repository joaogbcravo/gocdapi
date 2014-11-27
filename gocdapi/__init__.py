"""
About this library
==================

TODO

Installing gocdapi
=====================

TODO

Project Authors
===============

 * Joao Cravo (joaogbcravo@gmail.com)

Current code lives on github: TODO

"""
import pkg_resources
from gocdapi import (

    # Files
    agent, agents, configuration, custom_exceptions, go, gobase, pipeline, pipeline_group,
    pipeline_groups, stage
)

__all__ = [
    "agent", "agents", "configuration", "custom_exceptions", "go", "gobase", "pipeline", "pipeline_group",
    "pipeline_groups", "stage"
]
__docformat__ = "epytext"
__version__ = pkg_resources.working_set.by_key['gocdapi'].version
