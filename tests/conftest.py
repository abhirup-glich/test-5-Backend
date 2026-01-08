import pytest
from app import create_app
from unittest.mock import MagicMock
import sys

# Mock supabase before importing app
mock_supabase = MagicMock()
sys.modules['supabase'] = MagicMock()

@pytest.fixture
def app():
    # Patch the supabase client in utils
    with pytest.patch('app.utils.supabase_client.supabase', mock_supabase):
        app = create_app()
        app.config.update({
            "TESTING": True,
            "JWT_SECRET_KEY": "test-secret"
        })
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
