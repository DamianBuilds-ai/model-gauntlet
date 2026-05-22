import hmac
import hashlib


def make_token(account_id, secret):
    msg = str(account_id).encode("utf-8")
    return hmac.new(secret, msg, hashlib.sha256).hexdigest()


def verify_token(token, account_id, secret):
    expected = make_token(account_id, secret)
    return hmac.compare_digest(expected, token)
