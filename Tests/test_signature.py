import pytest
from .signature_wrapper import generate_keys, sign, verify

@pytest.fixture
def keys():
    return generate_keys()

@pytest.fixture
def message_ok():
    return b"This is a message"

@pytest.fixture
def message_wrong():
    return b"This is a wrong message"


def test_sign_verify(keys, message_ok):
    private_key, public_key = keys
    #sign
    signature = sign(message_ok, private_key)
    #verify
    verification_message = verify(signature, message_ok, public_key)
    assert verification_message is True

def test_verify_works(keys, message_ok):
    private_key, public_key = keys
    #sign
    signature = sign(message_ok, private_key)
    #verify
    verification_message = verify(signature, message_ok, public_key)
    assert verification_message is True

def test_verify_wrong_message(keys, message_ok, message_wrong):
    private_key, public_key = keys
    #sign
    signature = sign(message_ok, private_key)
    #verify
    verification_message = verify(signature, message_wrong, public_key)
    assert verification_message is False

def test_verify_wrong_signature(keys, message_ok, message_wrong):
    private_key, public_key = keys
    wrong_private_key, _ = generate_keys()
    #sign
    wrong_signature = sign(message_wrong, wrong_private_key)
    #verify
    verification_message = verify(wrong_signature, message_ok, public_key)
    assert verification_message is False

