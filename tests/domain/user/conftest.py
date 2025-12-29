from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from spotify_rag.domain.user import SpotifyUser


@register_fixture(name="spotify_user_factory")
class SpotifyUserFactory(ModelFactory[SpotifyUser]):
    __random_seed__ = 123
