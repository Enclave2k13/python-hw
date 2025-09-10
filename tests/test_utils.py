import json
from unittest.mock import mock_open
from unittest.mock import patch

from src.utils import retrieve_transaction_amount
from src.utils import retrieve_transactions_by_path

@patch('src.utils.parse_transaction')
def test_retrieve_transactions_by_path_success(mock_parse):
    """Позитивный тест: файл содержит корректный список словарей"""
    mock_data = '[{"id": 1}, {"id": 2}]'
    mock_parse.side_effect = lambda x, _: x

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = retrieve_transactions_by_path("fake_path.json")
        assert result == [{"id": 1}, {"id": 2}]


def test_retrieve_transactions_by_path_file_not_found():
    """Файл не найден — должен вернуться пустой список"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = retrieve_transactions_by_path("missing.json")
        assert result == []


def test_retrieve_transactions_by_path_invalid_json():
    """Файл содержит некорректный JSON — должен вернуться пустой список"""
    with (
        patch("builtins.open", mock_open(read_data="not a json")),
        patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)),
    ):
        result = retrieve_transactions_by_path("bad.json")
        assert result == []


def test_retrieve_transactions_by_path_not_a_list():
    """Файл содержит валидный JSON, но не список — вернётся пустой список"""
    mock_data = '{"id": 123}'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = retrieve_transactions_by_path("notalist.json")
        assert result == []


def test_retrieve_transaction_amount_rub():
    """Если валюта RUB, convert_amount не вызывается"""
    transaction = {"operationAmount": {"amount": 100.0, "currency": {"code": "RUB"}}, "date": "2024-01-01"}
    with patch("src.utils.convert_amount") as mock_convert:
        result = retrieve_transaction_amount(transaction)
        assert result == 100.0
        mock_convert.assert_not_called()


def test_retrieve_transaction_amount_usd_calls_convert():
    """Если валюта не RUB, convert_amount вызывается"""
    transaction = {"operationAmount": {"amount": 200.0, "currency": {"code": "USD"}}, "date": "2024-01-01"}

    with patch("src.utils.convert_amount", return_value=18000.0) as mock_convert:
        result = retrieve_transaction_amount(transaction)
        assert result == 18000.0
        mock_convert.assert_called_once_with(200.0, "USD", "RUB", "2024-01-01")
