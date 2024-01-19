import pytest
from rentomatic.application.app import create_app

@pytest.fixture
def app():
    app = create_app("testing")
    return app