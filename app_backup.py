

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from dotenv import load_dotenv
from encryption import encrypt_message
from database import (save_message, get_message_history, get_users_by_role, get_user_id, 
                     get_recent_conversations, search_messages, get_message_statistics, delete_message)
from ai_agent import ai_reply

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'secure_chat_secret_key_2024')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Track active users and their rooms
active_users = {}

def get_room_name(buyer_username, seller_username):
    """Generate unique room name for buyer-seller pair"""
    return f"{buyer_username}_{seller_username}"

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/api/contacts/<role>")
def get_contacts(role):
    """Get list of users by role"""
    if role not in ['buyer', 'seller']:
        return jsonify({"error": "Invalid role"}), 400
    
    users = get_users_by_role(role)
    return jsonify({"users": users})

@app.route("/api/history/<buyer_username>/<seller_username>")
def get_history(buyer_username, seller_username):
    """Get message history between two users"""
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    history = get_message_history(buyer_username, seller_username, limit, offset)
    return jsonify(history)

@app.route("/api/conversations/<username>")
def get_conversations(username):
    """Get recent conversations for a user"""
    limit = request.args.get('limit', 10, type=int)
    conversations = get_recent_conversations(username, limit)
    return jsonify({"conversations": conversations})

@app.route("/api/search")
def search():
    """Search messages within a conversation"""
    username = request.args.get('username')
    partner = request.args.get('partner')
    query = request.args.get('query')
    limit = request.args.get('limit', 20, type=int)
    
    if not all([username, partner, query]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    results = search_messages(username, partner, query, limit)
    return jsonify({"results": results})

@app.route("/api/statistics/<username>")
def get_statistics(username):
    """Get message statistics for a user"""
    days = request.args.get('days', 30, type=int)
    stats = get_message_statistics(username, days)
    return jsonify(stats)

@app.route("/api/delete-message/<int:message_id>", methods=['DELETE'])
def delete_message_route(message_id):
    """Delete a message"""
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    success = delete_message(message_id, username)
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to delete message"}), 403

@socketio.on("connect")
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    # Remove user from active users
    username_to_remove = None
    for username, sid in active_users.items():
        if sid == request.sid:
            username_to_remove = username
            break
    
    if username_to_remove:
        del active_users[username_to_remove]
        print(f"Client disconnected: {username_to_remove}")

@socketio.on("login")
def handle_login(data):
    username = data.get("username")
    password = data.get("password")
    
    print(f"Login attempt: {username}")
    
    # Validate user (simple password check for demo)
    if password != "soweto311" or not username:
        print(f"Login failed for {username}")
        emit("login_error", {"message": "Invalid credentials"})
        return
    
    # Add to active users
    active_users[username] = request.sid
    print(f"Login successful: {username}")
    emit("login_success", {"username": username})

@socketio.on("join_chat")
def handle_join_chat(data):
    username = data.get("username")
    partner_username = data.get("partner")
    
    if not username or not partner_username:
        return
    
    # Get user roles to determine room structure
    user_info = get_user_id(username)
    partner_info = get_user_id(partner_username)
    
    if not user_info or not partner_info:
        return
    
    user_id, user_role = user_info
    partner_id, partner_role = partner_info
    
    # Determine buyer and seller for room naming
    if user_role == 'buyer' and partner_role == 'seller':
        room = get_room_name(username, partner_username)
    elif user_role == 'seller' and partner_role == 'buyer':
        room = get_room_name(partner_username, username)
    else:
        return  # Only buyer-seller chats allowed
    
    # Join the private room
    join_room(room)
    emit("joined_chat", {"room": room, "partner": partner_username})
    
    # Load and send message history
    history_data = get_message_history(username, partner_username, limit=50)
    emit("chat_history", history_data)

@socketio.on("leave_chat")
def handle_leave_chat(data):
    username = data.get("username")
    partner_username = data.get("partner")
    
    if username and partner_username:
        user_info = get_user_id(username)
        partner_info = get_user_id(partner_username)
        
        if user_info and partner_info:
            user_id, user_role = user_info
            partner_id, partner_role = partner_info
            
            if user_role == 'buyer' and partner_role == 'seller':
                room = get_room_name(username, partner_username)
            elif user_role == 'seller' and partner_role == 'buyer':
                room = get_room_name(partner_username, username)
            else:
                return
            
            leave_room(room)

@socketio.on("send_message")
def handle_message(data):
    sender = data.get("sender")
    receiver = data.get("receiver")
    message = data.get("message")
    
    if not sender or not receiver or not message:
        return
    
    # Get user roles
    sender_info = get_user_id(sender)
    receiver_info = get_user_id(receiver)
    
    if not sender_info or not receiver_info:
        return
    
    sender_id, sender_role = sender_info
    receiver_id, receiver_role = receiver_info
    
    # Only allow buyer-seller communication
    if not ((sender_role == 'buyer' and receiver_role == 'seller') or 
            (sender_role == 'seller' and receiver_role == 'buyer')):
        return
    
    # Encrypt message before storing
    encrypted = encrypt_message(message)
    
    # Save to database
    if not save_message(sender, receiver, encrypted):
        emit("send_error", {"message": "Failed to save message"})
        return
    
    # Determine room for private messaging
    if sender_role == 'buyer' and receiver_role == 'seller':
        room = get_room_name(sender, receiver)
    else:  # seller to buyer
        room = get_room_name(receiver, sender)
    
    # Send message to private room only
    emit("receive_message", {
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": "now"  # Frontend will format
    }, room=room)
    
    # AI responds ONLY when buyer talks to seller
    if sender_role == 'buyer' and receiver_role == 'seller':
        # Generate AI response in background
        try:
            reply = ai_reply(message, receiver, sender)
            
            # Save AI message to database
            encrypted_reply = encrypt_message(reply)
            save_message(receiver, sender, encrypted_reply)
            
            # Send AI response to room
            emit("receive_message", {
                "sender": receiver,
                "receiver": sender,
                "message": reply,
                "timestamp": "now",
                "is_ai": True
            }, room=room)
            
        except Exception as e:
            print(f"AI response error: {e}")
            emit("ai_error", {"message": "AI unavailable"})

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5001,
        debug=False,
        allow_unsafe_werkzeug=True
    )
