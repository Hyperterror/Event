"""
Database Helper Module for Event Contact System
Handles all MySQL database operations using mysql.connector
"""

import mysql.connector as con
from config import Config
from datetime import datetime
import hashlib


class DatabaseHelper:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.mydb = con.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT,
                database="event"  # Your database name
            )
            self.mycursor = self.mydb.cursor(dictionary=True)
            print("✅ Database connected successfully!")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            self.mydb = None
            self.mycursor = None

    def close(self):
        """Close database connection"""
        if self.mycursor:
            self.mycursor.close()
        if self.mydb:
            self.mydb.close()

    # ==================== USER OPERATIONS ====================

    def register_user(self, first_name, last_name, mobile_no, username, password, role="participant"):
        """Register a new user"""
        try:
            # Hash password for security
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            query = """
            INSERT INTO users (first_name, last_name, mobile_no, username, rpassword, rrole)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, mobile_no, username, hashed_password, role)
            
            self.mycursor.execute(query, values)
            self.mydb.commit()
            
            return {"success": True, "user_id": self.mycursor.lastrowid}
        except con.IntegrityError:
            return {"success": False, "error": "Username already exists"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login_user(self, username, password):
        """Authenticate user login"""
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            query = """
            SELECT user_ID, first_name, last_name, mobile_no, username, rrole
            FROM users
            WHERE username = %s AND rpassword = %s
            """
            
            self.mycursor.execute(query, (username, hashed_password))
            user = self.mycursor.fetchone()
            
            if user:
                return {"success": True, "user": user}
            else:
                return {"success": False, "error": "Invalid credentials"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        try:
            query = "SELECT * FROM users WHERE user_ID = %s"
            self.mycursor.execute(query, (user_id,))
            return self.mycursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    # ==================== EVENT OPERATIONS ====================

    def create_event(self, title, category, event_description, start_date, end_date, 
                     start_time, end_time, event_status, event_code, organiser_id, type_of_event="conference"):
        """Create a new event"""
        try:
            query = """
            INSERT INTO eventz (title, category, event_description, start_date, end_date,
                               start_time, end_time, event_status, event_code, organiser_id, type_of_event)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (title, category, event_description, start_date, end_date,
                     start_time, end_time, event_status, event_code, organiser_id, type_of_event)
            
            self.mycursor.execute(query, values)
            self.mydb.commit()
            
            return {"success": True, "event_id": self.mycursor.lastrowid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_events(self):
        """Get all events"""
        try:
            query = """
            SELECT e.*, o.organiser_name
            FROM eventz e
            LEFT JOIN organiser o ON e.organiser_id = o.organiser_id
            ORDER BY e.start_date DESC
            """
            self.mycursor.execute(query)
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_event_by_id(self, event_id):
        """Get event details by ID"""
        try:
            query = """
            SELECT e.*, o.organiser_name, o.email as organiser_email
            FROM eventz e
            LEFT JOIN organiser o ON e.organiser_id = o.organiser_id
            WHERE e.event_id = %s
            """
            self.mycursor.execute(query, (event_id,))
            return self.mycursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_event_by_code(self, event_code):
        """Get event by event code"""
        try:
            query = "SELECT * FROM eventz WHERE event_code = %s"
            self.mycursor.execute(query, (event_code,))
            return self.mycursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_events_by_status(self, status):
        """Get events filtered by status"""
        try:
            query = """
            SELECT e.*, o.organiser_name
            FROM eventz e
            LEFT JOIN organiser o ON e.organiser_id = o.organiser_id
            WHERE e.event_status = %s
            ORDER BY e.start_date DESC
            """
            self.mycursor.execute(query, (status,))
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_user_events(self, user_id):
        """Get all events a user has joined"""
        try:
            query = """
            SELECT e.*, o.organiser_name
            FROM eventz e
            INNER JOIN joins j ON e.event_id = j.event_id
            LEFT JOIN organiser o ON e.organiser_id = o.organiser_id
            WHERE j.user_id = %s
            ORDER BY e.start_date DESC
            """
            self.mycursor.execute(query, (user_id,))
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    # ==================== JOIN EVENT OPERATIONS ====================

    def join_event(self, user_id, event_id):
        """User joins an event"""
        try:
            query = "INSERT INTO joins (user_id, event_id) VALUES (%s, %s)"
            self.mycursor.execute(query, (user_id, event_id))
            self.mydb.commit()
            return {"success": True}
        except con.IntegrityError:
            return {"success": False, "error": "Already joined this event"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_user_joined_event(self, user_id, event_id):
        """Check if user has joined an event"""
        try:
            query = "SELECT * FROM joins WHERE user_id = %s AND event_id = %s"
            self.mycursor.execute(query, (user_id, event_id))
            return self.mycursor.fetchone() is not None
        except Exception as e:
            print(f"Error: {e}")
            return False

    # ==================== ANNOUNCEMENT OPERATIONS ====================

    def create_announcement(self, announcement_text, author_username, event_id, 
                           file_name=None, file_type=None, venue_id=None):
        """Create a new announcement"""
        try:
            # Insert announcement
            query = """
            INSERT INTO announcements (announcement_text, author_username, file_name, file_type, venue_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (announcement_text, author_username, file_name, file_type, venue_id)
            
            self.mycursor.execute(query, values)
            announcement_id = self.mycursor.lastrowid
            
            # Link announcement to event
            link_query = "INSERT INTO Containz (event_id, announcement_id) VALUES (%s, %s)"
            self.mycursor.execute(link_query, (event_id, announcement_id))
            
            self.mydb.commit()
            return {"success": True, "announcement_id": announcement_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_event_announcements(self, event_id):
        """Get all announcements for an event"""
        try:
            query = """
            SELECT a.*
            FROM announcements a
            INNER JOIN Containz c ON a.announcement_id = c.announcement_id
            WHERE c.event_id = %s
            ORDER BY a.created_at DESC
            """
            self.mycursor.execute(query, (event_id,))
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    # ==================== CHAT OPERATIONS ====================

    def send_message(self, event_id, sender_username, chat_message_text, 
                    subevent_name="", idx_event_chat=0, idx_subevent_chat=0):
        """Send a chat message"""
        try:
            query = """
            INSERT INTO chat_messages (event_id, subevent_name, sender_username, 
                                      idx_event_chat, idx_subevent_chat, chat_message_text)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (event_id, subevent_name, sender_username, 
                     idx_event_chat, idx_subevent_chat, chat_message_text)
            
            self.mycursor.execute(query, values)
            self.mydb.commit()
            
            return {"success": True, "chat_id": self.mycursor.lastrowid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_event_chat(self, event_id, limit=50):
        """Get event chat messages (main event chat)"""
        try:
            query = """
            SELECT * FROM chat_messages
            WHERE event_id = %s AND subevent_name = ''
            ORDER BY created_at DESC
            LIMIT %s
            """
            self.mycursor.execute(query, (event_id, limit))
            messages = self.mycursor.fetchall()
            return list(reversed(messages))  # Return in chronological order
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_subevent_chat(self, event_id, subevent_name, limit=50):
        """Get subevent chat messages"""
        try:
            query = """
            SELECT * FROM chat_messages
            WHERE event_id = %s AND subevent_name = %s
            ORDER BY created_at DESC
            LIMIT %s
            """
            self.mycursor.execute(query, (event_id, subevent_name, limit))
            messages = self.mycursor.fetchall()
            return list(reversed(messages))
        except Exception as e:
            print(f"Error: {e}")
            return []

    # ==================== SUBEVENT OPERATIONS ====================

    def create_subevent(self, sub_event_name, description, event_id, venue_id=None):
        """Create a new subevent"""
        try:
            # Insert subevent
            query = """
            INSERT INTO sub_events (sub_event_name, decription, venue_id)
            VALUES (%s, %s, %s)
            """
            self.mycursor.execute(query, (sub_event_name, description, venue_id))
            sub_event_id = self.mycursor.lastrowid
            
            # Link subevent to event
            link_query = "INSERT INTO Have (event_id, sub_event_id) VALUES (%s, %s)"
            self.mycursor.execute(link_query, (event_id, sub_event_id))
            
            self.mydb.commit()
            return {"success": True, "sub_event_id": sub_event_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_event_subevents(self, event_id):
        """Get all subevents for an event"""
        try:
            query = """
            SELECT s.*
            FROM sub_events s
            INNER JOIN Have h ON s.sub_event_id = h.sub_event_id
            WHERE h.event_id = %s
            ORDER BY s.created_at DESC
            """
            self.mycursor.execute(query, (event_id,))
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    # ==================== ORGANISER OPERATIONS ====================

    def create_organiser(self, organiser_name, phone_number, email, post, user_id):
        """Create an organiser profile"""
        try:
            query = """
            INSERT INTO organiser (organiser_name, phone_number, email, post, user_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (organiser_name, phone_number, email, post, user_id)
            
            self.mycursor.execute(query, values)
            self.mydb.commit()
            
            return {"success": True, "organiser_id": self.mycursor.lastrowid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_organiser_by_user_id(self, user_id):
        """Get organiser details by user ID"""
        try:
            query = "SELECT * FROM organiser WHERE user_id = %s"
            self.mycursor.execute(query, (user_id,))
            return self.mycursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return None

    # ==================== UTILITY FUNCTIONS ====================

    def execute_query(self, query, params=None):
        """Execute a custom query"""
        try:
            if params:
                self.mycursor.execute(query, params)
            else:
                self.mycursor.execute(query)
            
            self.mydb.commit()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fetch_query(self, query, params=None):
        """Fetch results from a custom query"""
        try:
            if params:
                self.mycursor.execute(query, params)
            else:
                self.mycursor.execute(query)
            
            return self.mycursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []


# Singleton instance
_db_instance = None

def get_db():
    """Get database helper instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseHelper()
    return _db_instance
