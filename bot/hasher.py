from cryptography.fernet import Fernet


class Protector:
    """Method hides access to users passwords"""
    key = Fernet.generate_key()

    def encrypt(self, password: str) -> str:
        if password:
            return str(Fernet(self.key).encrypt(password.encode('utf-8')), 'utf-8')

    def decrypt(self, crypt) -> str:
        if crypt:
            return str(Fernet(self.key).decrypt(crypt.encode('utf-8')), 'utf-8')



