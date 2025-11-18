"""
Test Database Connection and Basic Operations
Run this script to verify your database setup
"""

from db_helper import get_db
from datetime import datetime, date, time

def test_connection():
    """Test database connection"""
    print("=" * 50)
    print("Testing Database Connection...")
    print("=" * 50)
    
    db = get_db()
    
    if db.mydb and db.mydb.is_connected():
        print("✅ Database connected successfully!")
        print(f"   Host: {db.mydb.server_host}")
        print(f"   Database: event")
        return True
    else:
        print("❌ Database connection failed!")
        return False

def test_tables():
    """Test if all required tables exist"""
    print("\n" + "=" * 50)
    print("Checking Database Tables...")
    print("=" * 50)
    
    db = get_db()
    
    required_tables = [
        'users', 'eventz', 'joins', 'announcements', 
        'chat_messages', 'sub_events', 'organiser',
        'registration', 'venue', 'speaker'
    ]
    
    try:
        db.mycursor.execute("SHOW TABLES")
        existing_tables = [table['Tables_in_event'] for table in db.mycursor.fetchall()]
        
        print(f"\nFound {len(existing_tables)} tables:")
        for table in existing_tables:
            status = "✅" if table in required_tables else "ℹ️"
            print(f"  {status} {table}")
        
        missing = set(required_tables) - set(existing_tables)
        if missing:
            print(f"\n⚠️  Missing tables: {', '.join(missing)}")
        else:
            print("\n✅ All required tables exist!")
        
        return len(missing) == 0
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def test_user_operations():
    """Test user registration and login"""
    print("\n" + "=" * 50)
    print("Testing User Operations...")
    print("=" * 50)
    
    db = get_db()
    
    # Test registration
    print("\n1. Testing user registration...")
    test_username = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    result = db.register_user(
        first_name="Test",
        last_name="User",
        mobile_no="+1234567890",
        username=test_username,
        password="testpass123",
        role="participant"
    )
    
    if result["success"]:
        print(f"   ✅ User registered successfully! User ID: {result['user_id']}")
        user_id = result["user_id"]
        
        # Test login
        print("\n2. Testing user login...")
        login_result = db.login_user(test_username, "testpass123")
        
        if login_result["success"]:
            print(f"   ✅ Login successful!")
            print(f"      Name: {login_result['user']['first_name']} {login_result['user']['last_name']}")
            print(f"      Role: {login_result['user']['rrole']}")
            return True
        else:
            print(f"   ❌ Login failed: {login_result['error']}")
            return False
    else:
        print(f"   ❌ Registration failed: {result['error']}")
        return False

def test_event_operations():
    """Test event creation and retrieval"""
    print("\n" + "=" * 50)
    print("Testing Event Operations...")
    print("=" * 50)
    
    db = get_db()
    
    # First, create an organiser
    print("\n1. Creating test organiser...")
    org_result = db.create_organiser(
        organiser_name="Test Organiser",
        phone_number="+1234567890",
        email="organiser@test.com",
        post="Event Manager",
        user_id=1  # Assuming user_id 1 exists
    )
    
    if not org_result["success"]:
        print(f"   ⚠️  Organiser creation skipped (may already exist)")
        organiser_id = 1  # Use existing
    else:
        print(f"   ✅ Organiser created! ID: {org_result['organiser_id']}")
        organiser_id = org_result["organiser_id"]
    
    # Create event
    print("\n2. Creating test event...")
    event_code = f"TEST{datetime.now().strftime('%Y%m%d')}"
    
    result = db.create_event(
        title="Test Event",
        category="Technology",
        event_description="This is a test event",
        start_date=date.today(),
        end_date=date.today(),
        start_time=time(9, 0),
        end_time=time(17, 0),
        event_status="upcoming",
        event_code=event_code,
        organiser_id=organiser_id
    )
    
    if result["success"]:
        print(f"   ✅ Event created successfully! Event ID: {result['event_id']}")
        
        # Test retrieval
        print("\n3. Testing event retrieval...")
        events = db.get_all_events()
        print(f"   ✅ Retrieved {len(events)} events from database")
        
        return True
    else:
        print(f"   ❌ Event creation failed: {result['error']}")
        return False

def test_announcement_operations():
    """Test announcement creation"""
    print("\n" + "=" * 50)
    print("Testing Announcement Operations...")
    print("=" * 50)
    
    db = get_db()
    
    # Get first event
    events = db.get_all_events()
    if not events:
        print("   ⚠️  No events found. Create an event first.")
        return False
    
    event_id = events[0]['event_id']
    
    print(f"\n1. Creating announcement for event {event_id}...")
    result = db.create_announcement(
        announcement_text="This is a test announcement!",
        author_username="testuser",
        event_id=event_id
    )
    
    if result["success"]:
        print(f"   ✅ Announcement created! ID: {result['announcement_id']}")
        
        # Retrieve announcements
        print("\n2. Retrieving announcements...")
        announcements = db.get_event_announcements(event_id)
        print(f"   ✅ Retrieved {len(announcements)} announcements")
        
        return True
    else:
        print(f"   ❌ Announcement creation failed: {result['error']}")
        return False

def test_chat_operations():
    """Test chat message operations"""
    print("\n" + "=" * 50)
    print("Testing Chat Operations...")
    print("=" * 50)
    
    db = get_db()
    
    # Get first event
    events = db.get_all_events()
    if not events:
        print("   ⚠️  No events found. Create an event first.")
        return False
    
    event_id = events[0]['event_id']
    
    print(f"\n1. Sending test message to event {event_id}...")
    result = db.send_message(
        event_id=event_id,
        sender_username="testuser",
        chat_message_text="Hello, this is a test message!",
        subevent_name="",
        idx_event_chat=1
    )
    
    if result["success"]:
        print(f"   ✅ Message sent! Chat ID: {result['chat_id']}")
        
        # Retrieve messages
        print("\n2. Retrieving chat messages...")
        messages = db.get_event_chat(event_id, limit=10)
        print(f"   ✅ Retrieved {len(messages)} messages")
        
        return True
    else:
        print(f"   ❌ Message sending failed: {result['error']}")
        return False

def run_all_tests():
    """Run all database tests"""
    print("\n" + "=" * 50)
    print("DATABASE CONNECTION TEST SUITE")
    print("=" * 50 + "\n")
    
    results = {
        "Connection": test_connection(),
        "Tables": test_tables(),
        "User Operations": test_user_operations(),
        "Event Operations": test_event_operations(),
        "Announcements": test_announcement_operations(),
        "Chat": test_chat_operations()
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("\n" + "=" * 50)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("\n🎉 All tests passed! Database is ready to use!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    run_all_tests()
