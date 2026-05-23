from dependency_injector import containers, providers

from .containers import (
    InfrastructureContainer,
    ServicesContainer,
    TestInfrastructureContainer,
)


class ProductionContainer(containers.DeclarativeContainer):
    """Main DI container wired for production with real external clients."""

    infrastructure = providers.Container(InfrastructureContainer)
    services = providers.Container(ServicesContainer, infrastructure=infrastructure)


class TestContainer(containers.DeclarativeContainer):
    """Main DI container wired for testing with in-memory fakes.

    Instantiate a fresh TestContainer per test so that each test gets its own
    set of Singleton fakes and an isolated vector store collection.
    """

    __test__ = False  # prevent pytest from collecting this as a test class

    infrastructure = providers.Container(TestInfrastructureContainer)
    services = providers.Container(ServicesContainer, infrastructure=infrastructure)


# Keep Container as an alias so existing imports don't break.
Container = ProductionContainer
