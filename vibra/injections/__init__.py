from vibra.utils import Settings

from .container import Container, ProductionContainer, TestContainer
from .containers import InfrastructureContainer, ServicesContainer, TestInfrastructureContainer

# Select the singleton container based on the current environment so that
# production always uses real clients and the test runner uses fakes without
# any extra fixture setup.
container = TestContainer() if Settings.ENVIRONMENT == "testing" else ProductionContainer()

__all__ = [
    "Container",
    "InfrastructureContainer",
    "ProductionContainer",
    "ServicesContainer",
    "TestContainer",
    "TestInfrastructureContainer",
    "container",
]
