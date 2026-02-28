import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from encryption import decrypt_message

# Load environment variables
load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'chatdb'),
        user=os.getenv('DB_USER', 'moturi311'),
        password=os.getenv('DB_PASSWORD', 'soweto311'),
        host=os.getenv('DB_HOST', 'localhost')
    )

def get_user_id(username):
    """Get user ID from username"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, role FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result if result else None

def get_or_create_conversation(buyer_id, seller_id):
    """Get existing conversation or create new one"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Try to get existing conversation
    cur.execute(
        "SELECT id FROM conversations WHERE buyer_id = %s AND seller_id = %s",
        (buyer_id, seller_id)
    )
    result = cur.fetchone()
    
    if result:
        conversation_id = result[0]
    else:
        # Create new conversation
        cur.execute(
            "INSERT INTO conversations (buyer_id, seller_id) VALUES (%s, %s) RETURNING id",
            (buyer_id, seller_id)
        )
        conversation_id = cur.fetchone()[0]
        conn.commit()
    
    cur.close()
    conn.close()
    return conversation_id

def save_message(sender_username, receiver_username, content):
    """Save encrypted message to database"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user IDs
    sender_info = get_user_id(sender_username)
    receiver_info = get_user_id(receiver_username)
    
    if not sender_info or not receiver_info:
        cur.close()
        conn.close()
        return False
    
    sender_id, sender_role = sender_info
    receiver_id, receiver_role = receiver_info
    
    # Determine buyer and seller for conversation
    if sender_role == 'buyer' and receiver_role == 'seller':
        buyer_id, seller_id = sender_id, receiver_id
    elif sender_role == 'seller' and receiver_role == 'buyer':
        buyer_id, seller_id = receiver_id, sender_id
    else:
        cur.close()
        conn.close()
        return False
    
    # Get or create conversation
    conversation_id = get_or_create_conversation(buyer_id, seller_id)
    
    # Insert message with timestamp
    cur.execute(
        "INSERT INTO messages (conversation_id, sender_id, receiver_id, encrypted_content, timestamp) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (conversation_id, sender_id, receiver_id, content, datetime.now())
    )
    
    message_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return message_id

def get_message_history(buyer_username, seller_username, limit=50, offset=0):
    """Get decrypted message history between buyer and seller with pagination"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user IDs
    buyer_info = get_user_id(buyer_username)
    seller_info = get_user_id(seller_username)
    
    if not buyer_info or not seller_info:
        cur.close()
        conn.close()
        return []
    
    buyer_id = buyer_info[0]
    seller_id = seller_info[0]
    
    # Get conversation
    cur.execute(
        "SELECT id FROM conversations WHERE buyer_id = %s AND seller_id = %s",
        (buyer_id, seller_id)
    )
    conversation_result = cur.fetchone()
    
    if not conversation_result:
        cur.close()
        conn.close()
        return []
    
    conversation_id = conversation_result[0]
    
    # Get messages with pagination
    cur.execute("""
        SELECT m.id, u.username, m.encrypted_content, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.timestamp ASC
        LIMIT %s OFFSET %s
    """, (conversation_id, limit, offset))
    
    messages = cur.fetchall()
    
    # Get total message count for pagination info
    cur.execute(
        "SELECT COUNT(*) FROM messages WHERE conversation_id = %s",
        (conversation_id,)
    )
    total_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    # Decrypt messages
    history = []
    for message_id, username, encrypted_content, timestamp in messages:
        try:
            decrypted_content = decrypt_message(encrypted_content)
            history.append({
                "id": message_id,
                "sender": username,
                "message": decrypted_content,
                "timestamp": timestamp
            })
        except Exception as e:
            print(f"Error decrypting message {message_id}: {e}")
            continue
    
    return {
        "messages": history,
        "total_count": total_count,
        "has_more": offset + limit < total_count
    }

def get_recent_conversations(username, limit=10):
    """Get recent conversations for a user"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user info
    user_info = get_user_id(username)
    if not user_info:
        cur.close()
        conn.close()
        return []
    
    user_id, user_role = user_info[0]
    
    # Get conversations where user is either buyer or seller
    if user_role == 'buyer':
        cur.execute("""
            SELECT c.id, u.username as partner_name, u.role as partner_role,
                   MAX(m.timestamp) as last_message_time,
                   COUNT(m.id) as message_count
            FROM conversations c
            JOIN users u ON (c.seller_id = u.id)
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.buyer_id = %s
            GROUP BY c.id, u.username, u.role
            ORDER BY last_message_time DESC NULLS LAST
            LIMIT %s
        """, (user_id, limit))
    else:  # seller
        cur.execute("""
            SELECT c.id, u.username as partner_name, u.role as partner_role,
                   MAX(m.timestamp) as last_message_time,
                   COUNT(m.id) as message_count
            FROM conversations c
            JOIN users u ON (c.buyer_id = u.id)
            LEFT JOIN messages m ON c.id = m.conversation_id
            WHERE c.seller_id = %s
            GROUP BY c.id, u.username, u.role
            ORDER BY last_message_time DESC NULLS LAST
            LIMIT %s
        """, (user_id, limit))
    
    conversations = []
    for conv_id, partner_name, partner_role, last_time, msg_count in cur.fetchall():
        conversations.append({
            "conversation_id": conv_id,
            "partner": partner_name,
            "partner_role": partner_role,
            "last_message_time": last_time,
            "message_count": msg_count or 0
        })
    
    cur.close()
    conn.close()
    return conversations

def search_messages(username, partner_username, query, limit=20):
    """Search messages within a conversation"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user IDs
    buyer_info = get_user_id(username) if username.startswith('buyer') else get_user_id(partner_username)
    seller_info = get_user_id(partner_username) if partner_username.startswith('seller') else get_user_id(username)
    
    if not buyer_info or not seller_info:
        cur.close()
        conn.close()
        return []
    
    buyer_id = buyer_info[0]
    seller_id = seller_info[0]
    
    # Get conversation
    cur.execute(
        "SELECT id FROM conversations WHERE buyer_id = %s AND seller_id = %s",
        (buyer_id, seller_id)
    )
    conversation_result = cur.fetchone()
    
    if not conversation_result:
        cur.close()
        conn.close()
        return []
    
    conversation_id = conversation_result[0]
    
    # Search messages (we need to decrypt to search, so we'll fetch and filter)
    cur.execute("""
        SELECT m.id, u.username, m.encrypted_content, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.timestamp DESC
        LIMIT %s
    """, (conversation_id, limit * 2))  # Get more to account for filtering
    
    messages = cur.fetchall()
    cur.close()
    conn.close()
    
    # Decrypt and search
    results = []
    for message_id, username, encrypted_content, timestamp in messages:
        try:
            decrypted_content = decrypt_message(encrypted_content)
            if query.lower() in decrypted_content.lower():
                results.append({
                    "id": message_id,
                    "sender": username,
                    "message": decrypted_content,
                    "timestamp": timestamp
                })
                if len(results) >= limit:
                    break
        except Exception as e:
            continue
    
    return results

def get_message_statistics(username, days=30):
    """Get message statistics for a user"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get user info
    user_info = get_user_id(username)
    if not user_info:
        cur.close()
        conn.close()
        return {}
    
    user_id, user_role = user_info[0]
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Get message statistics
    if user_role == 'buyer':
        cur.execute("""
            SELECT 
                COUNT(m.id) as total_messages,
                COUNT(DISTINCT c.seller_id) as unique_sellers,
                COUNT(DISTINCT DATE(m.timestamp)) as active_days
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.sender_id = %s OR m.receiver_id = %s
            AND m.timestamp >= %s
        """, (user_id, user_id, cutoff_date))
    else:  # seller
        cur.execute("""
            SELECT 
                COUNT(m.id) as total_messages,
                COUNT(DISTINCT c.buyer_id) as unique_buyers,
                COUNT(DISTINCT DATE(m.timestamp)) as active_days
            FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE m.sender_id = %s OR m.receiver_id = %s
            AND m.timestamp >= %s
        """, (user_id, user_id, cutoff_date))
    
    stats = cur.fetchone()
    cur.close()
    conn.close()
    
    return {
        "total_messages": stats[0] or 0,
        "unique_partners": stats[1] or 0,
        "active_days": stats[2] or 0,
        "period_days": days
    }

def delete_message(message_id, username):
    """Delete a message (only if user is sender)"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get message and verify sender
    cur.execute("""
        SELECT m.sender_id, u.username
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.id = %s
    """, (message_id,))
    
    result = cur.fetchone()
    if not result or result[1] != username:
        cur.close()
        conn.close()
        return False
    
    # Delete the message
    cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return True

def get_users_by_role(role):
    """Get all users with specific role"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE role = %s ORDER BY username", (role,))
    users = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return users
