# Secure Marketplace Chat System

A real-time encrypted messaging system with AI-powered seller responses for marketplace communications.

## Features

### 🔐 Security
- **End-to-end encryption** for all messages using Fernet symmetric encryption
- **Persistent encryption keys** stored securely
- **Private Socket.IO rooms** for buyer-seller conversations
- **No plain text storage** of messages in database

### 🤖 AI-Powered Sellers
- **5 unique seller personalities** with different communication styles:
  - **seller1** - TechPro Electronics: Professional, technical specifications
  - **seller2** - QuickDeal Store: Direct, business-focused, concise
  - **seller3** - FriendlyBob's Shop: Casual, humorous, friendly
  - **seller4** - Luxury Premium: Sophisticated, high-end service
  - **seller5** - Speedy Sales: Fast, efficient, no small talk
- **Conversation memory** - AI remembers last 5 messages for context
- **Personalized responses** based on buyer identity and conversation history

### 💬 Real-time Messaging
- **Instant message delivery** to intended recipients only
- **Private rooms** using format: `buyer_username_seller_username`
- **Message history** loading when opening conversations
- **WhatsApp-like UI** with proper timestamps and message alignment

### 🗄️ Database Structure
- **Normalized PostgreSQL schema** with proper foreign keys
- **Users table** with roles (buyer/seller)
- **Conversations table** for buyer-seller pairs
- **Messages table** with encrypted content
- **Optimized indexes** for performance

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- OpenRouter AI API key

### 2. Database Setup

```bash
# Create database
sudo -u postgres createdb chatdb

# Create user (if not exists)
sudo -u postgres createuser --interactive moturi311

# Set password
sudo -u postgres psql -c "ALTER USER moturi311 PASSWORD 'soweto311';"
```

### 3. Install Dependencies

```bash
# Clone or navigate to project directory
cd secure_market_chat

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
# Run schema setup
psql -h localhost -U moturi311 -d chatdb -f schema.sql
```

### 5. Configure Environment Variables

Create a `.env` file with your configuration:

```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=your-openrouter-api-key-here
AI_MODEL=qwen/qwen-2.5-7b-instruct

# Database Configuration
DB_NAME=chatdb
DB_USER=moturi311
DB_PASSWORD=soweto311
DB_HOST=localhost

# Flask Configuration
FLASK_SECRET_KEY=secure_chat_secret_key_2024
FLASK_DEBUG=True
```

**Important**: Keep your `.env` file secure and never commit it to version control.

### 6. Run Application

```bash
python app.py
```

The application will start on `http://localhost:5001`

## Usage

### Login
- **Username**: Select from dropdown (buyer1-5 or seller1-5)
- **Password**: `soweto311` (demo password)

### Chat Features
- **Buyers** can chat with any seller
- **Sellers** receive AI-powered responses automatically
- **Messages** are encrypted before storage
- **History** loads automatically when opening conversations

### Seller Personalities
Each seller has a unique communication style:
- **seller1**: Detailed technical explanations
- **seller2**: Short, business-focused responses
- **seller3**: Friendly, casual conversation
- **seller4**: Premium, luxury-focused tone
- **seller5**: Quick, efficient replies

## Architecture

### Backend Components
- **`app.py`** - Main Flask application with Socket.IO events
- **`database.py`** - Database operations and queries
- **`encryption.py`** - Message encryption/decryption
- **`ai_agent.py`** - AI response generation with personalities

### Frontend Components
- **`templates/chat.html`** - Single-page application
- **`static/style.css`** - Modern WhatsApp-like styling
- **Socket.IO client** - Real-time communication

### Database Schema
```sql
users (id, username, password, role)
conversations (id, buyer_id, seller_id)
messages (id, conversation_id, sender_id, receiver_id, encrypted_content, timestamp)
```

## Security Features

- **Message Encryption**: All messages encrypted using Fernet symmetric encryption
- **Private Rooms**: Socket.IO rooms ensure messages only reach intended recipients
- **No Global Broadcasting**: Messages sent only to specific buyer-seller pairs
- **Secure Storage**: Encrypted content stored in database, never plain text

## AI Integration

The system uses OpenRouter API with GPT-4o-mini for seller responses:

- **Context Awareness**: AI receives conversation history
- **Personality Consistency**: Each seller maintains unique communication style
- **Personalization**: Responses tailored to specific buyer interactions
- **Memory**: AI remembers previous messages in conversation

## Development

### File Structure
```
secure_market_chat/
├── app.py              # Main Flask application
├── database.py         # Database operations
├── encryption.py       # Message encryption
├── ai_agent.py         # AI response generation
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── chat.html      # Frontend application
└── static/
    └── style.css      # CSS styling
```

### Testing
- Test with different buyer-seller combinations
- Verify AI personality differences
- Check message encryption in database
- Test real-time message delivery

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials in `database.py`
   - Ensure database `chatdb` exists

2. **AI Not Responding**
   - Verify OpenRouter API key is valid
   - Check internet connection
   - Monitor console for API errors

3. **Messages Not Sending**
   - Check browser console for Socket.IO errors
   - Verify both users are online
   - Check database permissions

4. **Encryption Key Error**
   - Delete `encryption.key` file to regenerate
   - Ensure file write permissions

### Debug Mode
Run with debug enabled:
```bash
python app.py
```

Check browser console and terminal for detailed error messages.

## License

This project is for educational and demonstration purposes.
