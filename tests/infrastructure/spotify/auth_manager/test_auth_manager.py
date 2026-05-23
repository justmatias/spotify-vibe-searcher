from unittest.mock import MagicMock

import pytest

from vibra.domain.user import OAuthToken
from vibra.infrastructure.spotify.auth_manager import SpotifyAuthManager


@pytest.mark.usefixtures("setup_get_auth_url")
def test_auth_manager_get_auth_url(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    url = auth_manager.get_auth_url()

    assert url == "http://auth.url"
    mock_oauth_instance.get_authorize_url.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_exchange_code_success")
async def test_exchange_code_success(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = await auth_manager.exchange_code("code")
    assert isinstance(token, OAuthToken)
    assert token.access_token == "123"
    mock_oauth_instance.get_access_token.assert_called_with("code", as_dict=True)


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_exchange_code_failure")
async def test_exchange_code_failure(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = await auth_manager.exchange_code("code_fail")
    assert token is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_refresh_success")
async def test_refresh_success(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = await auth_manager.refresh("refresh_code")
    assert isinstance(token, OAuthToken)
    assert token.access_token == "new_123"
    mock_oauth_instance.refresh_access_token.assert_called_with("refresh_code")


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_refresh_failure")
async def test_refresh_failure(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = await auth_manager.refresh("refresh_code_fail")
    assert token is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_cached_token_missing")
async def test_cached_token_missing(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = await auth_manager.cached_token()
    assert token is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_cached_token_valid")
async def test_cached_token_valid(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = await auth_manager.cached_token()
    assert isinstance(token, OAuthToken)
    assert token.access_token == "cached"
    mock_oauth_instance.validate_token.assert_called_with(
        mock_oauth_instance.cache_handler.get_cached_token.return_value
    )
