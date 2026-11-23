"""Mocking tests: test the Groq wrapper without making real API calls."""
import pytest

from groq_chat import ask_groq


def make_fake_response(mocker, content="4"):
    """Build a response object with the same attributes used by ask_groq."""
    mock_choice = mocker.Mock()
    mock_choice.message.content = content

    mock_response = mocker.Mock()
    mock_response.choices = [mock_choice]
    return mock_response


def test_ask_groq_returns_mocked_answer(mocker):
    mock_response = make_fake_response(mocker, "4")
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    answer = ask_groq("What is 2+2?", client=mock_client)

    assert answer == "4"


def test_ask_groq_calls_api_with_expected_arguments(mocker):
    mock_response = make_fake_response(mocker, "4")
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    ask_groq("What is 2+2?", client=mock_client)

    mock_client.chat.completions.create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        max_tokens=1024,
    )


def test_ask_groq_propagates_api_error(mocker):
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.side_effect = Exception("API down")

    with pytest.raises(Exception, match="API down"):
        ask_groq("What is 2+2?", client=mock_client)


def test_ask_groq_rejects_empty_question(mocker):
    mock_client = mocker.Mock()

    with pytest.raises(ValueError, match="Question cannot be empty"):
        ask_groq("   ", client=mock_client)

    mock_client.chat.completions.create.assert_not_called()
