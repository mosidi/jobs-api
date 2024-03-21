from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if a plain password matches a hashed password.

        Args:
            plain_password (str): The plain password to be verified.
            hashed_password (str): The hashed password to be compared against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return password_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        A static method to generate a password hash.

        Parameters:
            password (str): The password to generate a hash for.

        Returns:
            str: The hashed password.
        """
        return password_context.hash(password)
