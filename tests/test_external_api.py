from unittest.mock import Mock
from unittest.mock import patch

from src.external_api import convert_amount


@patch("src.external_api.requests.get")
def test_convert_amount_success(mock_get):
    """Проверяем, что convert_amount возвращает корректный float из API"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 123.45}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_amount(100, "USD", "RUB", "2024-01-01")

    assert result == 123.45
    mock_get.assert_called_once()
