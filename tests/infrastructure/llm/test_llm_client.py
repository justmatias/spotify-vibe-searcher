# pylint: disable=protected-access
import pytest

from spotify_rag.infrastructure.llm import LLMClient


def test_client_lazy_initialization(llm_client: LLMClient) -> None:
    assert llm_client._client is None
    client = llm_client.client
    assert llm_client.client is client


def test_client_reuses_instance(llm_client: LLMClient) -> None:
    client1 = llm_client.client
    client2 = llm_client.client
    assert client1 is client2


@pytest.mark.vcr
def test_generate_simple_prompt(llm_client: LLMClient, simple_prompt: str) -> None:
    response = llm_client.generate(simple_prompt)
    assert isinstance(response, str)
    assert response == "Paris."


@pytest.mark.vcr
def test_generate_analysis_prompt(llm_client: LLMClient, analysis_prompt: str) -> None:
    response = llm_client.generate(analysis_prompt)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.vcr
def test_generate_returns_stripped_content(llm_client: LLMClient) -> None:
    response = llm_client.generate("Say hello")
    assert not response.startswith(" ")
    assert not response.endswith(" ")


def test_generate_handles_api_error(llm_client_with_api_error: LLMClient) -> None:
    """Test that generate properly wraps API errors."""
    with pytest.raises(RuntimeError, match="Failed to generate text"):
        llm_client_with_api_error.generate("test prompt")
