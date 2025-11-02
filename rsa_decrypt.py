from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logger = logging.getLogger(__name__)


class RSADecrypt:
    """Handles RSA decryption operations"""
    
    @staticmethod
    def decrypt_message(encrypted_b64, private_key_pem):
        """
        Decrypt a message using RSA private key
        
        Args:
            encrypted_b64 (str): Base64 encoded encrypted message
            private_key_pem (str): Private key in PEM format
            
        Returns:
            str: Decrypted original message
        """
        try:
            encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
            private_key = RSA.import_key(private_key_pem.encode('utf-8'))
            cipher = PKCS1_OAEP.new(private_key)
            decrypted = cipher.decrypt(encrypted)
            decrypted_str = decrypted.decode('utf-8')
            
            logger.info(f"Message decrypted successfully")
            return decrypted_str
            
        except ValueError as e:
            logger.error(f"Decryption failed - invalid key or corrupted data: {e}")
            raise Exception("Decryption failed - invalid private key or corrupted message")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise Exception(f"Decryption error: {str(e)}")