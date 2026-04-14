"""Dependency injection module."""

from .container import Container
from .containers import InfrastructureContainer, ServicesContainer

# Singleton container instance
container = Container()

__all__ = ["Container", "InfrastructureContainer", "ServicesContainer", "container"]
