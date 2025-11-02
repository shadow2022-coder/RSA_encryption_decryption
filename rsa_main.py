
"""RSA Main Logic - Manages key generation and message flow"""

from Crypto.PublicKey import RSA
from rsa_encrypt import RSAEncrypt
from rsa_decrypt import RSADecrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSAChat:
    """Main RSA Chat Application Logic"""
    
    def __init__(self):
        """Initialize RSA Chat"""
        self.alice_private_key = None
        self.alice_public_key = None
        self.bob_private_key = None
        self.bob_public_key = None
        self.messages = []
        
        logger.info("RSA Chat initialized")
    
    def generate_keys_for_user(self, username):
        """
        Generate RSA-2048 key pair for a user
        
        Args:
            username (str): Username ('alice' or 'bob')
            
        Returns:
            dict: Public and private keys
        """
        try:
            logger.info(f"Generating keys for {username}")
            
            key = RSA.generate(2048)
            private_key = key.export_key().decode('utf-8')
            public_key = key.publickey().export_key().decode('utf-8')
            
            if username.lower() == 'alice':
                self.alice_private_key = private_key
                self.alice_public_key = public_key
            elif username.lower() == 'bob':
                self.bob_private_key = private_key
                self.bob_public_key = public_key
            
            logger.info(f"Keys generated for {username}")
            
            return {
                'username': username,
                'public_key': public_key[:100] + "...",
                'private_key': private_key[:100] + "...",
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Key generation failed for {username}: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def send_message(self, sender, message, recipient_public_key):
        """
        Send an encrypted message
        
        Args:
            sender (str): Sender username
            message (str): Message to send
            recipient_public_key (str): Recipient's public key
            
        Returns:
            dict: Encrypted message data
        """
        try:
            encrypted = RSAEncrypt.encrypt_message(message, recipient_public_key)
            
            msg_data = {
                'sender': sender,
                'message': message,
                'encrypted': encrypted,
                'status': 'encrypted'
            }
            self.messages.append(msg_data)
            
            logger.info(f"Message from {sender} encrypted and stored")
            
            return {
                'status': 'success',
                'encrypted_message': encrypted,
                'message_size': {
                    'original': len(message),
                    'encrypted': len(encrypted)
                }
            }
            
        except Exception as e:
            logger.error(f"Send message failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def receive_message(self, encrypted_message, private_key):
        """
        Receive and decrypt a message
        
        Args:
            encrypted_message (str): Encrypted message
            private_key (str): Recipient's private key
            
        Returns:
            dict: Decrypted message data
        """
        try:
            decrypted = RSADecrypt.decrypt_message(encrypted_message, private_key)
            
            logger.info(f"Message decrypted successfully")
            
            return {
                'status': 'success',
                'decrypted_message': decrypted
            }
            
        except Exception as e:
            logger.error(f"Receive message failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_message_history(self):
        """Get all messages"""
        return {
            'total_messages': len(self.messages),
            'messages': self.messages
        }
    
    def get_key_info(self):
        """Get information about generated keys"""
        return {
            'alice': {
                'public_key_length': len(self.alice_public_key) if self.alice_public_key else 0,
                'private_key_length': len(self.alice_private_key) if self.alice_private_key else 0,
                'key_size': '2048 bits'
            },
            'bob': {
                'public_key_length': len(self.bob_public_key) if self.bob_public_key else 0,
                'private_key_length': len(self.bob_private_key) if self.bob_private_key else 0,
                'key_size': '2048 bits'
            }
        }


rsa_chat = RSAChat()
