"""Dependency injection container for Spotify RAG."""

from dependency_injector import containers

from .containers import InfrastructureContainer, ServicesContainer


class Container(containers.DeclarativeContainer):
    """Main application dependency injection container"""

    infrastructure = containers.Container(InfrastructureContainer)
    services = containers.Container(ServicesContainer)
