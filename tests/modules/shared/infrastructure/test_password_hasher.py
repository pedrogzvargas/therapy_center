from modules.shared.password_hasher.infraestructure import Argon2PasswordHasher


def test_password_hasher():
    password = "Test"
    argon2_password_hasher = Argon2PasswordHasher()
    hashed_password = argon2_password_hasher.hash(password=password)
    correct_password = argon2_password_hasher.verify(hashed_password=hashed_password, password=password)
    assert correct_password is True


def test_wrong_password_verifier():
    password = "Test"
    argon2_password_hasher = Argon2PasswordHasher()
    hashed_password = argon2_password_hasher.hash(password=password)
    correct_password = argon2_password_hasher.verify(hashed_password=hashed_password, password="")
    assert correct_password is False
