import pytest
from app.config import Settings


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("APP_CONFIG__DATABASE__HOST", "localhost")
    monkeypatch.setenv("APP_CONFIG__DATABASE__PORT", "5432")
    monkeypatch.setenv("APP_CONFIG__DATABASE__NAME", "test_db")
    monkeypatch.setenv("APP_CONFIG__DATABASE__USER", "test_user")
    monkeypatch.setenv("APP_CONFIG__DATABASE__PASSWORD", "secret")
    monkeypatch.setenv("APP_CONFIG__DATABASE__ECHO", "true")
    monkeypatch.setenv("APP_CONFIG__DATABASE__ECHO_POOL", "false")
    monkeypatch.setenv("APP_CONFIG__DATABASE__POOL_SIZE", "5")
    monkeypatch.setenv("APP_CONFIG__DATABASE__MAX_OVERFLOW", "10")


def test_settings_loading(mock_env):
    
    settings = Settings()

    db = settings.database
    assert db.host == "localhost"
    assert db.port == 5432
    assert db.name == "test_db"
    assert db.user == "test_user"
    assert db.password == "secret"
    assert db.echo is True
    assert db.echo_pool is False
    assert db.pool_size == 5
    assert db.max_overflow == 10
    assert db.url == "postgresql+asyncpg://test_user:secret@localhost:5432/test_db"
