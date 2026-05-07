import pytest
from unittest.mock import patch
from test import XchangeSystem


@pytest.fixture
def system():
    app = XchangeSystem()

    # тестова база даних
    app.db = {
        "users": {
            "admin": {
                "password": "admin",
                "role": "Адміністратор",
                "name": "Admin"
            },
            "trader1": {
                "password": "123",
                "role": "Трейдер",
                "name": "Trader"
            }
        },
        "accounts": {}
    }

    return app


def test_successful_login(system):
    with patch('builtins.input', side_effect=['admin', 'admin']):
        result = system.login()

    assert result is True
    assert system.current_user["role"] == "Адміністратор"


def test_failed_login(system):
    with patch(
        'builtins.input',
        side_effect=[
            'wrong', 'wrong',
            'wrong', 'wrong',
            'wrong', 'wrong'
        ]
    ):
        result = system.login()

    assert result is False


def test_add_user(system):
    system.current_user = {
        "role": "Адміністратор",
        "name": "Admin"
    }

    with patch(
        'builtins.input',
        side_effect=['newuser', 'pass123', 'Test User']
    ):
        system.add_user()

    assert "newuser" in system.db["users"]
    assert system.db["users"]["newuser"]["name"] == "Test User"


def test_add_account(system):
    system.current_user = {
        "role": "Адміністратор",
        "name": "Admin"
    }

    with patch(
        'builtins.input',
        side_effect=['Ivan Petrov', '1000']
    ):
        system.add_account()

    assert len(system.db["accounts"]) == 1

    account = list(system.db["accounts"].values())[0]

    assert account["client_name"] == "Ivan Petrov"
    assert account["balance"] == '1000'


def test_execute_trade(system):
    system.current_user = {
        "role": "Трейдер",
        "name": "Trader"
    }

    system.db["accounts"]["ACC1000"] = {
        "client_name": "Client",
        "balance": "5000",
        "history": []
    }

    with patch(
        'builtins.input',
        side_effect=[
            'ACC1000',
            'BTC/USDT',
            'Купівля',
            '0.5'
        ]
    ):
        system.execute_trade()

    history = system.db["accounts"]["ACC1000"]["history"]

    assert len(history) == 1
    assert history[0]["asset"] == 'BTC/USDT'
    assert history[0]["action"] == 'Купівля'


def test_view_nonexistent_account(system, capsys):
    with patch('builtins.input', side_effect=['ACC9999']):
        system.view_account()

    captured = capsys.readouterr()

    assert "Рахунок не знайдено" in captured.out