import pytest
import time
from .jwt_wrapper import authenticate, decode, check_expired

# we don't really authenticate

@pytest.fixture()
def test_authenticate():
    valid_token = authenticate("admin", "password")
    return valid_token

@pytest.fixture
def test_decode(test_authenticate):
    decoded = decode(test_authenticate)
    return decoded

def test_incorrect_password():
    invalid_token = authenticate("admin", "incorrectpass")
    assert invalid_token is None

def test_incorrect_user():
    invalid_token = authenticate("someuser", "password")
    assert invalid_token is None

# check expiration time of the JWT
def test_valid_token_not_expired(test_decode):
    assert check_expired(test_decode["exp"]) is False

def test_expired(test_decode):
    time.sleep(1)
    assert check_expired(test_decode["exp"]) is True

