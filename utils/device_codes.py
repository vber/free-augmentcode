import os
import uuid
import secrets


def generate_machine_id() -> str:
    """
    Generate a random 64-character hex string for machine ID.
    Similar to using /dev/urandom in bash but using Python's cryptographic functions.
    
    Returns:
        str: A 64-character hexadecimal string
    """
    # Generate 32 random bytes (which will become 64 hex characters)
    random_bytes = secrets.token_bytes(32)
    # Convert to hexadecimal string
    return random_bytes.hex()


def generate_device_id() -> str:
    """
    Generate a random UUID v4 for device ID.
    
    Returns:
        str: A lowercase UUID v4 string in the format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        where x is any hexadecimal digit and y is one of 8, 9, A, or B
    """
    # Generate a random UUID v4
    device_id = str(uuid.uuid4())
    return device_id.lower()


if __name__ == "__main__":
    # Example usage
    print(f"Machine ID: {generate_machine_id()}")
    print(f"Device ID: {generate_device_id()}") 