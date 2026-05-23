from dependency_injector import containers, providers

from .containers import InfrastructureContainer, ServicesContainer


class Container(containers.DeclarativeContainer):
    infrastructure = providers.Container(InfrastructureContainer)
    services = providers.Container(ServicesContainer, infrastructure=infrastructure)
