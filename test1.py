from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
# ===== KEY GENERATION =====
print("Step 1: Generate RSA-2048 Keys")
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
# ===== ENCRYPTION =====
print("Step 2: Encrypt Message 'HELLO'")
message = b"HELLO"
cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
encrypted = cipher.encrypt(message)
encrypted_b64 = base64.b64encode(encrypted).decode()
print(f"Original: {message}")
print(f"Encrypted (Base64): {encrypted_b64[:50]}...")
# ===== DECRYPTION =====
print("Step 3: Decrypt Message")
cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
decrypted = cipher.decrypt(base64.b64decode(encrypted_b64))
print(f"Decrypted: {decrypted}")
print(f"Match: {message == decrypted} ")