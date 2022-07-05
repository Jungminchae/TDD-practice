import pytest


@pytest.fixture
def sample_emails():
    return [
        ["test1@EXAMPLE.com", "test1@example.com"],
        ["Test2@Example.com", "Test2@example.com"],
        ["TEST3@EXAMPLE.com", "TEST3@example.com"],
        ["test4@example.com", "test4@example.com"],
    ]
