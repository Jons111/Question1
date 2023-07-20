import asyncio
import aiohttp


def test_logs_with_valid_container_name(mock_connector, mock_session):
    """Test that the `logs()` function returns the logs for a valid container name."""
    mock_connector.return_value = mock_session
    mock_session.get.return_value = aiohttp.Response(
        status=200, content="foobar"
    )

    result = asyncio.run(logs("cont", "name"))

    assert result == ("name", "foobar")


def test_logs_with_invalid_container_name(mock_connector, mock_session):
    """Test that the `logs()` function raises an exception for an invalid container name."""
    mock_connector.return_value = mock_session
    mock_session.get.return_value = aiohttp.Response(
        status=404, content="Container not found"
    )

    with pytest.raises(aiohttp.ClientError):
        asyncio.run(logs("cont", "name"))


def test_logs_with_connection_error(mock_connector, mock_session):
    """Test that the `logs()` function raises an exception for a connection error."""
    mock_connector.side_effect = OSError(errno=111, message="Connection refused")

    with pytest.raises(OSError):
        asyncio.run(logs("cont", "name"))