import os

import pytest
from gsoc2 import Gsoc2Client


@pytest.fixture(scope="module")
def client():
    gsoc2_client = Gsoc2Client(
        token=os.environ.get("GSOC2_TOKEN"), token_json=os.environ.get("GSOC2_TOKEN_JSON"), site_url=os.environ.get("SITE_URL"), debug=True
    )

    gsoc2_client.create_secret("KEY_ONE", "KEY_ONE_VAL")
    gsoc2_client.create_secret("KEY_ONE", "KEY_ONE_VAL_PERSONAL", type="personal")
    gsoc2_client.create_secret("KEY_TWO", "KEY_TWO_VAL")

    # gsoc2_client.create_secret("TESTOO", "sssss", path="/foo", environment="dev")

    yield gsoc2_client

    gsoc2_client.delete_secret("KEY_ONE")
    gsoc2_client.delete_secret("KEY_TWO")
    gsoc2_client.delete_secret("KEY_THREE")

def test_get_overriden_personal_secret(client: Gsoc2Client):
    secret = client.get_secret("KEY_ONE")
    assert secret.secret_name == "KEY_ONE"
    assert secret.secret_value == "KEY_ONE_VAL_PERSONAL"
    assert secret.type == "personal"


def test_get_shared_secret_specified(client: Gsoc2Client):
    secret = client.get_secret("KEY_ONE", type="shared")
    assert secret.secret_name == "KEY_ONE"
    assert secret.secret_value == "KEY_ONE_VAL"
    assert secret.type == "shared"


def test_get_shared_secret(client: Gsoc2Client):
    secret = client.get_secret("KEY_TWO")
    assert secret.secret_name == "KEY_TWO"
    assert secret.secret_value == "KEY_TWO_VAL"
    assert secret.type == "shared"


def test_create_shared_secret(client: Gsoc2Client):
    secret = client.create_secret("KEY_THREE", "KEY_THREE_VAL")
    assert secret.secret_name == "KEY_THREE"
    assert secret.secret_value == "KEY_THREE_VAL"
    assert secret.type == "shared"


def test_create_personal_secret(client: Gsoc2Client):
    client.create_secret("KEY_FOUR", "KEY_FOUR_VAL")
    personal_secret = client.create_secret(
        "KEY_FOUR", "KEY_FOUR_VAL_PERSONAL", type="personal"
    )

    assert personal_secret.secret_name == "KEY_FOUR"
    assert personal_secret.secret_value == "KEY_FOUR_VAL_PERSONAL"
    assert personal_secret.type == "personal"


def test_update_shared_secret(client: Gsoc2Client):
    secret = client.update_secret("KEY_THREE", "FOO")

    assert secret.secret_name == "KEY_THREE"
    assert secret.secret_value == "FOO"
    assert secret.type == "shared"


def test_update_personal_secret(client: Gsoc2Client):
    secret = client.update_secret("KEY_FOUR", "BAR", type="personal")
    assert secret.secret_name == "KEY_FOUR"
    assert secret.secret_value == "BAR"
    assert secret.type == "personal"


def test_delete_personal_secret(client: Gsoc2Client):
    secret = client.delete_secret("KEY_FOUR", type="personal")
    assert secret.secret_name == "KEY_FOUR"
    assert secret.secret_value == "BAR"
    assert secret.type == "personal"


def test_delete_shared_secret(client: Gsoc2Client):
    secret = client.delete_secret("KEY_FOUR")
    assert secret.secret_name == "KEY_FOUR"
    assert secret.secret_value == "KEY_FOUR_VAL"
    assert secret.type == "shared"


def test_encrypt_decrypt_symmetric(client: Gsoc2Client):
    plaintext = "The quick brown fox jumps over the lazy dog"
    key = client.create_symmetric_key()

    ciphertext, iv, tag = client.encrypt_symmetric(plaintext, key)
    cleartext = client.decrypt_symmetric(ciphertext, key, iv, tag)
    assert plaintext == cleartext
