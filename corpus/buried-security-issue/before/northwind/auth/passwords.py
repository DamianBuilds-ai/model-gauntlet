import bcrypt


def hash_password(plaintext):
    return bcrypt.hashpw(plaintext.encode("utf-8"), bcrypt.gensalt())


def check_password(plaintext, hashed):
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed)
