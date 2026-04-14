from dependency_injector import containers, providers

from .containers import InfrastructureContainer, ServicesContainer


class Container(containers.DeclarativeContainer):
    """Main application dependency injection container"""

    infrastructure = providers.Container(InfrastructureContainer)
    services = providers.Container(ServicesContainer, infrastructure=infrastructure)
