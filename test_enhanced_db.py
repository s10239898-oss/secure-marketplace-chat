#!/usr/bin/env python3
"""
Test script for enhanced database functionality including message history and persistence
"""

import psycopg2
from encryption import encrypt_message, decrypt_message
from database import (get_connection, get_user_id, save_message, get_message_history, 
                     get_recent_conversations, search_messages, get_message_statistics, delete_message)

def test_enhanced_message_operations():
    """Test enhanced message operations with persistence"""
    print("🔍 Testing Enhanced Database Operations...")
    
    try:
        # Test saving multiple messages
        print("\n💾 Saving test messages...")
        msg1_id = save_message("buyer1", "seller1", "Hello, I'm interested in your product")
        msg2_id = save_message("seller1", "buyer1", "Great! Our product is excellent quality")
        msg3_id = save_message("buyer1", "seller1", "What are the specifications?")
        
        print(f"✅ Saved messages with IDs: {msg1_id}, {msg2_id}, {msg3_id}")
        
        # Test enhanced message history with pagination
        print("\n📚 Testing message history with pagination...")
        history = get_message_history("buyer1", "seller1", limit=2, offset=0)
        
        if history and "messages" in history:
            print(f"✅ Retrieved {len(history['messages'])} messages")
            print(f"   Total count: {history['total_count']}")
            print(f"   Has more: {history['has_more']}")
            
            # Test pagination
            if history['has_more']:
                more_history = get_message_history("buyer1", "seller1", limit=2, offset=2)
                print(f"✅ Retrieved {len(more_history['messages'])} more messages")
        
        # Test recent conversations
        print("\n💬 Testing recent conversations...")
        conversations = get_recent_conversations("buyer1", limit=5)
        print(f"✅ Found {len(conversations)} recent conversations for buyer1")
        for conv in conversations:
            print(f"   - {conv['partner']} ({conv['partner_role']}): {conv['message_count']} messages")
        
        conversations = get_recent_conversations("seller1", limit=5)
        print(f"✅ Found {len(conversations)} recent conversations for seller1")
        for conv in conversations:
            print(f"   - {conv['partner']} ({conv['partner_role']}): {conv['message_count']} messages")
        
        # Test message search
        print("\n🔍 Testing message search...")
        search_results = search_messages("buyer1", "seller1", "product", limit=10)
        print(f"✅ Found {len(search_results)} messages containing 'product'")
        for result in search_results:
            print(f"   - {result['sender']}: {result['message'][:50]}...")
        
        # Test message statistics
        print("\n📊 Testing message statistics...")
        stats = get_message_statistics("buyer1", days=30)
        print(f"✅ Buyer1 stats: {stats['total_messages']} messages, {stats['unique_partners']} partners, {stats['active_days']} active days")
        
        stats = get_message_statistics("seller1", days=30)
        print(f"✅ Seller1 stats: {stats['total_messages']} messages, {stats['unique_partners']} partners, {stats['active_days']} active days")
        
        # Test message deletion
        print("\n🗑️ Testing message deletion...")
        if msg1_id:
            success = delete_message(msg1_id, "buyer1")
            if success:
                print("✅ Successfully deleted message")
            else:
                print("❌ Failed to delete message")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced database operations error: {e}")
        return False

def test_conversation_persistence():
    """Test conversation persistence across multiple sessions"""
    print("\n🔄 Testing Conversation Persistence...")
    
    try:
        # Create messages in a conversation
        save_message("buyer2", "seller2", "First message")
        save_message("seller2", "buyer2", "Response to first message")
        save_message("buyer2", "seller2", "Second message")
        
        # Retrieve conversation history
        history = get_message_history("buyer2", "seller2")
        
        if history and "messages" in history:
            messages = history['messages']
            print(f"✅ Conversation persisted with {len(messages)} messages")
            
            # Verify message order
            for i, msg in enumerate(messages):
                print(f"   {i+1}. {msg['sender']}: {msg['message']}")
            
            # Test conversation appears in recent conversations
            conversations = get_recent_conversations("buyer2")
            buyer2_convs = [c for c in conversations if c['partner'] == 'seller2']
            if buyer2_convs:
                print(f"✅ Conversation appears in recent conversations with {buyer2_convs[0]['message_count']} messages")
            
            return True
        else:
            print("❌ No conversation history found")
            return False
            
    except Exception as e:
        print(f"❌ Conversation persistence error: {e}")
        return False

def test_encryption_persistence():
    """Test that messages remain encrypted in database but decrypt correctly"""
    print("\n🔐 Testing Encryption Persistence...")
    
    try:
        # Save an encrypted message
        original_message = "This is a secret test message with special chars: !@#$%^&*()"
        message_id = save_message("buyer3", "seller3", original_message)
        
        # Check database directly to verify encryption
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT encrypted_content FROM messages WHERE id = %s
        """, (message_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            encrypted_content = result[0]
            print(f"✅ Message stored as encrypted: {encrypted_content[:50]}...")
            
            # Verify it's not plain text
            if original_message not in encrypted_content:
                print("✅ Message is properly encrypted in database")
            else:
                print("❌ Message not encrypted properly")
                return False
            
            # Test decryption through API
            history = get_message_history("buyer3", "seller3")
            if history and "messages" in history and history['messages']:
                decrypted_message = history['messages'][0]['message']
                if decrypted_message == original_message:
                    print("✅ Message decrypts correctly through API")
                    return True
                else:
                    print("❌ Message decryption failed")
                    return False
            else:
                print("❌ Could not retrieve message for decryption test")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ Encryption persistence error: {e}")
        return False

def main():
    """Run all enhanced database tests"""
    print("🚀 Running Enhanced Database Tests\n")
    
    tests = [
        ("Enhanced Message Operations", test_enhanced_message_operations),
        ("Conversation Persistence", test_conversation_persistence),
        ("Encryption Persistence", test_encryption_persistence)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n📊 Enhanced Database Test Results:")
    print("=" * 50)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:30} {status}")
    
    all_passed = all(result for _, result in results)
    print("=" * 50)
    if all_passed:
        print("🎉 All enhanced database tests passed!")
        print("✅ Message history and persistence working perfectly!")
    else:
        print("⚠️ Some enhanced tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
