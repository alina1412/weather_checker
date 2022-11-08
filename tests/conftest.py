import pytest

from weather_app import app as flask_app


@pytest.fixture(scope="module")
def test_client():
    """Create a test client using the Flask
    application configured for testing"""
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
