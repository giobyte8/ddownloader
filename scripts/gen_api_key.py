import secrets


def get_token():
    return secrets.token_urlsafe(64)

print(get_token())
