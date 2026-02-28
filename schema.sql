-- Database Schema for Secure Marketplace Chat
-- Drop existing tables if they exist
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table with proper roles
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('buyer', 'seller')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table to track buyer-seller pairs
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    seller_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(buyer_id, seller_id)
);

-- Messages table with encryption and proper foreign keys
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    encrypted_content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_conversations_buyer ON conversations(buyer_id);
CREATE INDEX idx_conversations_seller ON conversations(seller_id);

-- Insert sample users
INSERT INTO users (username, password, role) VALUES
('buyer1', 'soweto311', 'buyer'),
('buyer2', 'soweto311', 'buyer'),
('buyer3', 'soweto311', 'buyer'),
('buyer4', 'soweto311', 'buyer'),
('buyer5', 'soweto311', 'buyer'),
('seller1', 'soweto311', 'seller'),
('seller2', 'soweto311', 'seller'),
('seller3', 'soweto311', 'seller'),
('seller4', 'soweto311', 'seller'),
('seller5', 'soweto311', 'seller');
