from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logger = logging.getLogger(__name__)


class RSAEncrypt:
    """Handles RSA encryption operations"""
    
    @staticmethod
    def encrypt_message(message, public_key_pem):
        """
        Encrypt a message using RSA public key
        
        Args:
            message (str): Message to encrypt
            public_key_pem (str): Public key in PEM format
            
        Returns:
            str: Base64 encoded encrypted message
        """
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            
            public_key = RSA.import_key(public_key_pem.encode('utf-8'))
            cipher = PKCS1_OAEP.new(public_key)
            encrypted = cipher.encrypt(message)
            encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
            
            logger.info(f"Message encrypted successfully")
            return encrypted_b64
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise Exception(f"Encryption error: {str(e)}")