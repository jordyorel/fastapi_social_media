from passlib.context import CryptContext


pdw_contexte = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password: str):
    return pdw_contexte.hash(password)


def verify(plain_password, hashed_password):
    return pdw_contexte.verify(plain_password, hashed_password)
