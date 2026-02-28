#!/usr/bin/env python3
"""
Test script to verify database and basic functionality
"""

import psycopg2
from encryption import encrypt_message, decrypt_message
from database import get_connection, get_user_id, save_message, get_message_history

def test_database():
    """Test database connection and basic operations"""
    print("🔍 Testing database connection...")
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Test basic query
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        print(f"✅ Database connected! Found {user_count} users")
        
        # Test user lookup
        cur.execute("SELECT username, role FROM users WHERE username = 'buyer1'")
        user = cur.fetchone()
        if user:
            print(f"✅ User lookup works: {user[0]} ({user[1]})")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def test_encryption():
    """Test encryption/decryption"""
    print("\n🔐 Testing encryption...")
    
    try:
        test_message = "Hello, this is a test message!"
        encrypted = encrypt_message(test_message)
        decrypted = decrypt_message(encrypted)
        
        if test_message == decrypted:
            print("✅ Encryption/decryption works!")
            return True
        else:
            print("❌ Encryption/decryption failed!")
            return False
            
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        return False

def test_message_operations():
    """Test message saving and retrieval"""
    print("\n💬 Testing message operations...")
    
    try:
        # Test saving a message
        success = save_message("buyer1", "seller1", "Test message from buyer to seller")
        if success:
            print("✅ Message saved successfully!")
        else:
            print("❌ Failed to save message")
            return False
        
        # Test retrieving message history
        history = get_message_history("buyer1", "seller1", limit=5)
        if history:
            print(f"✅ Retrieved {len(history)} messages from history")
            print(f"   Latest: {history[-1]['message']}")
        else:
            print("⚠️ No messages found in history")
        
        return True
        
    except Exception as e:
        print(f"❌ Message operations error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Secure Chat System Tests\n")
    
    tests = [
        ("Database", test_database),
        ("Encryption", test_encryption), 
        ("Message Operations", test_message_operations)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n📊 Test Results:")
    print("=" * 40)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(result for _, result in results)
    print("=" * 40)
    if all_passed:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
