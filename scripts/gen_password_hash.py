import sys
from werkzeug.security import generate_password_hash


def get_hash(password: str) -> str:
    return generate_password_hash(password)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/gen_password_hash.py <password>")
        sys.exit(1)

    print(get_hash(sys.argv[1]))
