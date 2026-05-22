import hmac
import hashlib
import secrets


def make_token(account_id, secret):
    nonce = secrets.token_hex(8)
    msg = f"{account_id}:{nonce}".encode("utf-8")
    mac = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return f"{nonce}.{mac}"


def verify_token(token, account_id, secret):
    nonce, _, mac = token.partition(".")
    msg = f"{account_id}:{nonce}".encode("utf-8")
    expected = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, mac)
