"""Flask Web Application for RSA Chat Demo"""

from flask import Flask, render_template, request, jsonify
from rsa_main import rsa_chat
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template('index.html')


@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    """Generate RSA keys for a user"""
    try:
        data = request.json
        username = data.get('username', 'user')
        
        result = rsa_chat.generate_keys_for_user(username)
        
        logger.info(f"Keys generated for {username}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error generating keys: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Send an encrypted message"""
    try:
        data = request.json
        sender = data.get('sender')
        message = data.get('message')
        recipient = data.get('recipient')
        
        recipient_public_key = None
        if recipient.lower() == 'bob':
            recipient_public_key = rsa_chat.bob_public_key
        elif recipient.lower() == 'alice':
            recipient_public_key = rsa_chat.alice_public_key
        
        if not recipient_public_key:
            return jsonify({'status': 'error', 'message': 'Recipient key not found'}), 400
        
        result = rsa_chat.send_message(sender, message, recipient_public_key)
        
        logger.info(f"Message from {sender} sent")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/receive-message', methods=['POST'])
def receive_message():
    """Receive and decrypt a message"""
    try:
        data = request.json
        encrypted_message = data.get('encrypted_message')
        recipient = data.get('recipient')
        
        recipient_private_key = None
        if recipient.lower() == 'bob':
            recipient_private_key = rsa_chat.bob_private_key
        elif recipient.lower() == 'alice':
            recipient_private_key = rsa_chat.alice_private_key
        
        if not recipient_private_key:
            return jsonify({'status': 'error', 'message': 'Recipient private key not found'}), 400
        
        result = rsa_chat.receive_message(encrypted_message, recipient_private_key)
        
        logger.info(f"Message received and decrypted for {recipient}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error receiving message: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get all messages"""
    try:
        return jsonify(rsa_chat.get_message_history())
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/keys-info', methods=['GET'])
def keys_info():
    """Get keys information"""
    try:
        return jsonify(rsa_chat.get_key_info())
    except Exception as e:
        logger.error(f"Error getting keys info: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear all messages and reset"""
    try:
        global rsa_chat
        from rsa_main import RSAChat
        rsa_chat = RSAChat()
        
        return jsonify({'status': 'success', 'message': 'Chat cleared'})
    except Exception as e:
        logger.error(f"Error clearing chat: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 RSA Chat Web Application")
    print("="*60)
    print("Starting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)