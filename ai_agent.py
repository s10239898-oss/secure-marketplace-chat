import requests
from database import get_connection
from encryption import decrypt_message

OPENROUTER_API_KEY = "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"

SELLER_PERSONALITIES = {
    "seller1": {
        "name": "TechPro Electronics",
        "personality": "You are a polite and professional electronics seller. You provide detailed technical specifications, offer excellent customer service, and always maintain a business-like tone. You address customers by name and are very knowledgeable about your products.",
        "style": "professional_technical"
    },
    "seller2": {
        "name": "QuickDeal Store",
        "personality": "You are a direct, no-nonsense business seller. You give short, precise answers and focus on closing deals quickly. You are efficient and professional but keep conversations brief and to the point.",
        "style": "direct_business"
    },
    "seller3": {
        "name": "FriendlyBob's Shop",
        "personality": "You are a very friendly and casual seller who loves to joke and build rapport with customers. You use humor, informal language, and create a relaxed shopping atmosphere. You make customers feel like friends.",
        "style": "friendly_casual"
    },
    "seller4": {
        "name": "Luxury Premium",
        "personality": "You are a luxury brand expert with a sophisticated and premium tone. You emphasize quality, exclusivity, and high-end service. You use elegant language and focus on the premium aspects of your products.",
        "style": "luxury_premium"
    },
    "seller5": {
        "name": "Speedy Sales",
        "personality": "You are extremely fast and efficient. You provide quick, direct responses with no small talk. Your goal is rapid communication and immediate answers. You are helpful but very concise.",
        "style": "fast_efficient"
    }
}

def get_conversation_history(buyer_id, seller_id, limit=10):
    """Get last N messages between buyer and seller for context"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT m.sender_id, u.username, m.encrypted_content, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        JOIN conversations c ON m.conversation_id = c.id
        WHERE (c.buyer_id = %s AND c.seller_id = %s) OR (c.buyer_id = %s AND c.seller_id = %s)
        ORDER BY m.timestamp DESC
        LIMIT %s
    """, (buyer_id, seller_id, seller_id, buyer_id, limit))
    
    messages = cur.fetchall()
    cur.close()
    conn.close()
    
    # Decrypt messages and reverse to chronological order
    history = []
    for msg in reversed(messages):
        sender_id, username, encrypted_content, timestamp = msg
        decrypted_content = decrypt_message(encrypted_content)
        history.append({
            "sender": username,
            "message": decrypted_content,
            "timestamp": timestamp
        })
    
    return history

def get_user_id(username):
    """Get user ID from username"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def ai_reply(message, seller_username, buyer_username=None):
    """Generate AI response with personality and conversation context"""
    seller_info = SELLER_PERSONALITIES.get(seller_username, {
        "name": "Helpful Seller",
        "personality": "You are a helpful marketplace seller.",
        "style": "helpful"
    })
    
    # Get conversation history for context
    buyer_id = get_user_id(buyer_username) if buyer_username else None
    seller_id = get_user_id(seller_username)
    
    conversation_context = ""
    if buyer_id and seller_id:
        history = get_conversation_history(buyer_id, seller_id, limit=5)
        if history:
            conversation_context = "\n\nRecent conversation history:\n"
            for msg in history:
                conversation_context += f"{msg['sender']}: {msg['message']}\n"
    
    # Build system prompt with personality and context
    system_prompt = f"""{seller_info['personality']}
    
Your name is {seller_info['name']}. You are chatting with {buyer_username or 'a customer'}.
{conversation_context}

Respond naturally as {seller_info['name']}, maintaining your personality style ({seller_info['style']}). 
Be helpful and address the customer's needs while staying in character."""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }
        )
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    except Exception as e:
        print(f"AI API Error: {e}")
        return f"Sorry, I'm having trouble responding right now. Please try again later."
