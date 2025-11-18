import streamlit as st
from datetime import datetime, timedelta, date, time as dt_time
import uuid
import mysql.connector as con
import time
from config import Config
from db_helper import get_db

# Initialize database connection
@st.cache_resource
def init_database():
    """Initialize database connection (cached)"""
    return get_db()


# Page configuration
st.set_page_config(
    page_title="Event Contact System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global font styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Event Card with Hover Effect */
    .event-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #FF6B6B 0%, #FFE66D 100%);
        transition: height 0.4s ease;
    }
    
    .event-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
        border-color: #FF6B6B;
    }
    
    .event-card:hover::before {
        height: 8px;
    }
    
    .ongoing-card::before {
        background: linear-gradient(90deg, #06D6A0 0%, #118AB2 100%);
    }
    
    .upcoming-card::before {
        background: linear-gradient(90deg, #F72585 0%, #B5179E 100%);
    }
    
    .completed-card::before {
        background: linear-gradient(90deg, #4CC9F0 0%, #4361EE 100%);
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Custom button classes */
    .create-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .join-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        background: #f8f9fa;
        border: none;
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Message bubble styling */
    .message-bubble {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .my-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    
    /* Role badge styling */
    .role-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
    }
    
    .core-badge {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
    }
    
    .participant-badge {
        background: linear-gradient(135deg, #A8E6CF 0%, #7BC8A4 100%);
        color: #2c3e50;
        box-shadow: 0 2px 8px rgba(168, 230, 207, 0.3);
    }
    
    /* Announcement styling */
    .announcement-box {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFF3CD 100%);
        border-left: 5px solid #FFB800;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.2rem 0;
        box-shadow: 0 3px 10px rgba(255, 184, 0, 0.1);
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Schedule item styling */
    .schedule-item {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .schedule-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    h1 {
        color: #1a1a1a;
        font-weight: 800;
        font-size: 2.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 700;
        font-size: 1.8rem;
        font-family: 'Inter', sans-serif;
    }
    
    h3 {
        color: #34495e;
        font-weight: 600;
        font-size: 1.4rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Paragraph styling */
    p {
        font-size: 1rem;
        line-height: 1.7;
        color: #4a5568;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px;
        padding: 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    /* User header card */
    .user-header-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.25);
        color: white;
    }
    
    /* Action buttons container */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def get_role_badge(role):
    """Return HTML for role badge"""
    role_classes = {
        "admin": "admin-badge",
        "core": "core-badge",
        "participant": "participant-badge"
    }
    return f'<span class="role-badge {role_classes.get(role.lower(), "participant-badge")}">{role.upper()}</span>'

def check_permission(event_id, user_role, required_roles):
    """Check if user has permission based on role"""
    return user_role.lower() in [r.lower() for r in required_roles]

def login_signup_page():
    load_custom_css()
    
    # Custom CSS for login/register forms - Dark theme with transparent inputs
    st.markdown("""
    <style>
    /* Remove extra borders and clean up input fields */
    .stTextInput > div > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div > input {
        background: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        color: #e2e8f0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background: rgba(102, 126, 234, 0.05) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Label styling */
    .stTextInput > label {
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Form container - transparent with subtle border */
    [data-testid="stForm"] {
        background: transparent;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Login/Register page specific */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    
    /* Submit button in forms */
    [data-testid="stForm"] button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    [data-testid="stForm"] button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Page title */
    .login-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        text-align: center;
    }
    
    /* Tab styling for dark theme */
    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: white !important;
    }
    
    /* Subheader styling */
    h3 {
        color: #e2e8f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-title">
            <h1>🎯 Event Contact System</h1>
            <p class="login-subtitle">Connect, Collaborate, Celebrate</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("<h3 style='color: #2d3748; font-weight: 600; margin-bottom: 1.5rem;'>Welcome Back! 👋</h3>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="your.email@example.com", label_visibility="visible")
                password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="visible")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if email and password:
                        db = init_database()
                        result = db.login_user(email, password)
                        
                        if result["success"]:
                            user = result["user"]
                            st.session_state.logged_in = True
                            st.session_state.user_id = user["user_ID"]
                            st.session_state.user_name = f"{user['first_name']} {user['last_name']}"
                            st.session_state.user_email = user["username"]
                            st.session_state.user_contact = user["mobile_no"]
                            st.session_state.user_role = user["rrole"]
                            st.session_state.current_page = "events"
                            st.success("✅ Login successful!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
                    else:
                        st.error("⚠️ Please enter both email and password!")
        
        with tab2:
            st.markdown("<h3 style='color: #2d3748; font-weight: 600; margin-bottom: 1.5rem;'>Create Your Account ✨</h3>", unsafe_allow_html=True)
            
            with st.form("signup_form"):
                name = st.text_input("Full Name", placeholder="John Doe", label_visibility="visible")
                email = st.text_input("Email Address", placeholder="john.doe@example.com", label_visibility="visible")
                contact = st.text_input("Contact Number", placeholder="+1 234 567 8900", label_visibility="visible")
                password = st.text_input("Password", type="password", placeholder="Create a strong password", label_visibility="visible")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", label_visibility="visible")
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    submitted = st.form_submit_button("Register", use_container_width=True)
                
                if submitted:
                    if not all([name, email, contact, password, confirm_password]):
                        st.error("⚠️ All fields are required!")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match!")
                    elif len(password) < 6:
                        st.error("⚠️ Password must be at least 6 characters!")
                    else:
                        db = init_database()
                        
                        # Split name into first and last
                        name_parts = name.strip().split()
                        first_name = name_parts[0]
                        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                        
                        # Register user
                        result = db.register_user(
                            first_name=first_name,
                            last_name=last_name,
                            mobile_no=contact,
                            username=email,  # Using email as username
                            password=password,
                            role="participant"
                        )
                        
                        if result["success"]:
                            # Auto-login after registration
                            st.session_state.logged_in = True
                            st.session_state.user_id = result["user_id"]
                            st.session_state.user_email = email
                            st.session_state.user_name = name
                            st.session_state.user_contact = contact
                            st.session_state.user_role = "participant"
                            st.session_state.current_page = "events"
                            st.success("✅ Account created successfully! Redirecting...")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")

def join_event_modal():
    """Modal for joining an event with event code and role"""
    st.subheader("🎫 Join an Event")
    
    with st.form("join_event_form"):
        event_code = st.text_input("Event Code", placeholder="Enter the event code (e.g., TECH2024)")
        event_name = st.text_input("Event Name", placeholder="Enter event name")
        role = st.selectbox("Your Role", ["Participant", "Core", "Admin"])
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Join Event", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if cancel:
            st.session_state.show_join_modal = False
            st.rerun()
        
        if submitted:
            if not event_code:
                st.error("⚠️ Please enter an event code!")
                return
            
            db = init_database()
            
            # Find event by code
            found_event = db.get_event_by_code(event_code.upper())
            
            if found_event:
                # Check if already joined
                already_joined = db.check_user_joined_event(
                    st.session_state.user_id,
                    found_event["event_id"]
                )
                
                if already_joined:
                    st.warning("⚠️ You have already joined this event!")
                else:
                    # Join event in database
                    result = db.join_event(
                        user_id=st.session_state.user_id,
                        event_id=found_event["event_id"]
                    )
                    
                    if result["success"]:
                        # Update role in Joins table
                        db.execute_query(
                            "UPDATE joins SET user_role = %s WHERE user_id = %s AND event_id = %s",
                            (role.lower(), st.session_state.user_id, found_event["event_id"])
                        )
                        
                        st.success(f"✅ Successfully joined {found_event['title']} as {role}!")
                        st.session_state.show_join_modal = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
            else:
                st.error("❌ Event not found! Please check the event code.")

def create_event_page():
    """Create a new event"""
    load_custom_css()
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.current_page = "events"
            st.rerun()
    
    st.title("➕ Create New Event")
    st.markdown("<p style='color: #7f8c8d;'>Fill in the details to create your event</p>", unsafe_allow_html=True)
    
    st.divider()
    
    with st.form("create_event_form"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            title = st.text_input("🎯 Event Title *", placeholder="e.g., Tech Conference 2024")
            event_code = st.text_input("🎫 Event Code *", placeholder="e.g., TECH2024 (Unique code for participants)")
            start_date = st.date_input("📅 Start Date *")
            status = st.selectbox("🏷️ Status *", ["upcoming", "ongoing", "completed"])
        
        with col_form2:
            description = st.text_area("📝 Description *", placeholder="Describe your event...", height=100)
            end_date = st.date_input("📅 End Date *")
            category = st.selectbox("🏷️ Category", ["Technology", "Business", "Education", "Entertainment", "Sports", "Other"])
        
        general_info = st.text_area("ℹ️ General Information (Optional)", 
                                    placeholder="Add any additional information about the event...",
                                    height=100)
        
        st.divider()
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
        with col_btn2:
            submitted = st.form_submit_button("✨ Create Event", use_container_width=True)
        
        if submitted:
            if not all([event_code, title, description]):
                st.error("⚠️ Please fill in all required fields (marked with *)!")
                return
            
            # Validate dates
            if end_date < start_date:
                st.error("❌ End date cannot be before start date!")
                return
            
            db = init_database()
            
            # Check if event code already exists
            existing_event = db.get_event_by_code(event_code.upper())
            if existing_event:
                st.error("❌ Event code already exists! Please use a unique code.")
                return
            
            # First, create or get organiser profile
            organiser = db.get_organiser_by_user_id(st.session_state.user_id)
            
            if not organiser:
                # Create organiser profile
                org_result = db.create_organiser(
                    organiser_name=st.session_state.user_name,
                    phone_number=st.session_state.user_contact,
                    email=st.session_state.user_email,
                    post="Event Organiser",
                    user_id=st.session_state.user_id
                )
                
                if not org_result["success"]:
                    st.error(f"❌ Error creating organiser profile: {org_result['error']}")
                    return
                
                organiser_id = org_result["organiser_id"]
            else:
                organiser_id = organiser["organiser_id"]
            
            # Create event in database
            result = db.create_event(
                title=title,
                category=category,
                event_description=description,
                start_date=start_date,
                end_date=end_date,
                start_time=dt_time(9, 0),  # Default start time
                end_time=dt_time(17, 0),  # Default end time
                event_status=status,
                event_code=event_code.upper(),
                organiser_id=organiser_id,
                type_of_event="conference"
            )
            
            if result["success"]:
                event_id = result["event_id"]
                
                # Automatically join the event as admin
                join_result = db.join_event(st.session_state.user_id, event_id)
                
                if join_result["success"]:
                    # Set role to admin
                    db.execute_query(
                        "UPDATE joins SET user_role = %s WHERE user_id = %s AND event_id = %s",
                        ("admin", st.session_state.user_id, event_id)
                    )
                
                st.success("✅ Event created successfully! You are the admin.")
                time.sleep(1)
                st.session_state.current_page = "events"
                st.rerun()
            else:
                st.error(f"❌ Error creating event: {result['error']}")

def events_page():
    """Main events page with filtering"""
    load_custom_css()
    
    # Action buttons with custom styling
    st.markdown("""
    <style>
    .action-btn-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        justify-content: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(2) button {
            background: linear-gradient(135deg, #06D6A0 0%, #118AB2 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            border-radius: 15px !important;
            box-shadow: 0 6px 20px rgba(6, 214, 160, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="column"]:nth-child(2) button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(6, 214, 160, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🎫 Join Event", use_container_width=True, key="join_event_btn"):
            st.session_state.show_join_modal = True
            st.rerun()
    
    with col3:
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(3) button {
            background: linear-gradient(135deg, #F72585 0%, #B5179E 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            border-radius: 15px !important;
            box-shadow: 0 6px 20px rgba(247, 37, 133, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="column"]:nth-child(3) button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 30px rgba(247, 37, 133, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("➕ Create Event", use_container_width=True, key="create_event_btn"):
            st.session_state.current_page = "create_event"
            st.rerun()
    
    # Show join modal if needed
    if st.session_state.get("show_join_modal", False):
        join_event_modal()
        return
    
    st.divider()
    
    # Filter events
    col_filter1, col_filter2 = st.columns([3, 1])
    with col_filter1:
        filter_option = st.selectbox(
            "🔍 Filter Events:",
            ["All Events", "My Events", "Ongoing", "Upcoming", "Completed"],
            key="event_filter"
        )
    
    # Get events from database based on filter
    db = init_database()
    
    if filter_option == "All Events":
        events = db.get_all_events()
    elif filter_option == "My Events":
        events = db.get_user_events(st.session_state.user_id)
    else:
        events = db.get_events_by_status(filter_option.lower())
    
    # Display events
    if not events:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #718096;">📭 No Events Available</h2>
            <p style="color: #a0aec0; font-size: 1.1rem;">There are no events to display at the moment.</p>
            <p style="color: #a0aec0;">Create a new event or join an existing one using an event code!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display event cards
    for event in events:
        event_id = event["event_id"]
        
        # Determine gradient based on status
        gradient_map = {
            "ongoing": "linear-gradient(90deg, #06D6A0 0%, #118AB2 100%)",
            "upcoming": "linear-gradient(90deg, #F72585 0%, #B5179E 100%)",
            "completed": "linear-gradient(90deg, #4CC9F0 0%, #4361EE 100%)"
        }
        
        status_gradient = gradient_map.get(event["event_status"], "linear-gradient(90deg, #FF6B6B 0%, #FFE66D 100%)")
        
        # Check if user is part of this event
        is_member = db.check_user_joined_event(st.session_state.user_id, event_id)
        
        # Get user role for this event
        user_role = "participant"
        if is_member:
            role_query = "SELECT user_role FROM joins WHERE user_id = %s AND event_id = %s"
            role_result = db.fetch_query(role_query, (st.session_state.user_id, event_id))
            if role_result:
                user_role = role_result[0].get("user_role", "participant")
        
        # Status badge with color
        status_emoji = {
            "ongoing": "🟢 LIVE",
            "upcoming": "🟡 UPCOMING", 
            "completed": "🔴 COMPLETED"
        }
        
        # Get counts from database
        announcements_count = len(db.get_event_announcements(event_id))
        subevents_count = len(db.get_event_subevents(event_id))
        messages_count = len(db.get_event_chat(event_id, limit=1000))
        
        # Create event card using Streamlit components instead of HTML
        with st.container():
            # Status badge
            col_title, col_status = st.columns([3, 1])
            with col_title:
                st.subheader(f"🎯 {event['title']}")
                if is_member:
                    st.markdown(get_role_badge(user_role), unsafe_allow_html=True)
            with col_status:
                st.markdown(f"**{status_emoji.get(event['event_status'], '🟡 UPCOMING')}**")
            
            st.write(f"📝 {event['event_description']}")
            st.write(f"📅 **{event['start_date']}** to **{event['end_date']}**")
            st.write(f"🎫 Event Code: `{event['event_code']}`")
        
        # Stats and action button
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1.5, 1.5, 1])
        
        with col1:
            st.metric("📢 Announcements", announcements_count)
        with col2:
            st.metric("🎪 Subevents", subevents_count)
        with col3:
            st.metric("📅 Schedule", 0)  # Will implement schedule later
        with col4:
            st.metric("💬 Messages", messages_count)
        with col5:
            st.write("")
            if is_member:
                if st.button("📖 Open", key=f"view_{event_id}", use_container_width=True):
                    st.session_state.current_event = event_id
                    st.session_state.current_page = "event_details"
                    st.rerun()
            else:
                if st.button("🎫 Join", key=f"join_{event_id}", use_container_width=True):
                    st.session_state.show_join_modal = True
                    st.rerun()
        
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

def event_details_page():
    """Detailed event view with multiple sections"""
    event_id = st.session_state.get("current_event")
    
    db = init_database()
    
    # Get event from database
    event = db.get_event_by_id(event_id)
    
    if not event:
        st.error("Event not found!")
        st.session_state.current_page = "events"
        st.rerun()
        return
    
    # Header with back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Events"):
            st.session_state.current_page = "events"
            st.rerun()
    
    with col2:
        st.title(f"🎯 {event['title']}")
        st.write(f"*{event['event_description']}*")
        
        # Event status and info
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Status", event['event_status'].title())
        with col_info2:
            st.metric("Event Code", event['event_code'])
        with col_info3:
            st.metric("Organizer", event.get('organiser_name', 'Unknown'))
    
    # Get user role for this event
    role_query = "SELECT user_role FROM joins WHERE user_id = %s AND event_id = %s"
    role_result = db.fetch_query(role_query, (st.session_state.user_id, event_id))
    user_role = role_result[0].get("user_role", "participant") if role_result else "participant"
    
    # Display user role
    st.markdown(f"**Your Role:** {get_role_badge(user_role)}", unsafe_allow_html=True)
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📢 Announcements", 
        "📅 Schedule", 
        "🎪 Subevents", 
        "💬 Event Chat",
        "ℹ️ General Info"
    ])
    
    # Announcements Tab
    with tab1:
        st.header("📢 Announcements")
        
        # Add announcement - Only Admin and Core can post
        if check_permission(event_id, user_role, ["admin", "core"]):
            with st.expander("➕ Post New Announcement", expanded=False):
                with st.form("add_announcement"):
                    announcement_text = st.text_area("Announcement Message", placeholder="Share important updates with all participants...")
                    announcement_file = st.file_uploader("📎 Attach Image/File (Optional)", 
                                                       type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'],
                                                       key="announcement_file")
                    
                    col_btn1, col_btn2 = st.columns([1, 4])
                    with col_btn1:
                        submitted = st.form_submit_button("📤 Post", use_container_width=True)
                    
                    if submitted and announcement_text:
                        # Store file info if uploaded
                        file_name = announcement_file.name if announcement_file else None
                        file_type = announcement_file.type if announcement_file else None
                        
                        # Create announcement in database
                        result = db.create_announcement(
                            announcement_text=announcement_text,
                            author_username=st.session_state.user_email,
                            event_id=event_id,
                            file_name=file_name,
                            file_type=file_type
                        )
                        
                        if result["success"]:
                            st.success("✅ Announcement posted successfully!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
        else:
            st.info("ℹ️ Only Admin and Core members can post announcements.")
        
        st.divider()
        
        # Display announcements from database
        announcements = db.get_event_announcements(event_id)
        
        if not announcements:
            st.info("📭 No announcements yet.")
        else:
            for announcement in announcements:
                with st.container():
                    # Format timestamp
                    timestamp = announcement['created_at'].strftime('%Y-%m-%d %H:%M') if hasattr(announcement['created_at'], 'strftime') else str(announcement['created_at'])[:16]
                    
                    st.markdown(f"""
                    <div class="announcement-box">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>👤 {announcement['author_username']}</strong>
                            </div>
                            <small style="color: #7f8c8d;">🕒 {timestamp}</small>
                        </div>
                        <p style="margin-top: 0.8rem; font-size: 1.05rem;">{announcement['announcement_text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if announcement.get('file_name'):
                        st.info(f"📎 Attachment: **{announcement['file_name']}**")
                    
                    st.write("")
                    
                    if announcement.get("has_file"):
                        st.info(f"📎 Attachment: **{announcement.get('filename', 'File')}**")
                    
                    if idx < len(event["announcements"]) - 1:
                        st.write("")
    
    # Schedule Tab
    with tab2:
        st.header("📅 Event Schedule")
        
        # Add schedule item - Only Admin and Core can add
        if check_permission(event, ["admin", "core"]):
            with st.expander("➕ Add Schedule Item", expanded=False):
                with st.form("add_schedule"):
                    col1, col2 = st.columns(2)
                    with col1:
                        schedule_date = st.date_input("📅 Date")
                    with col2:
                        schedule_time = st.time_input("🕐 Time")
                    
                    schedule_title = st.text_input("📌 Activity Title", placeholder="e.g., Opening Ceremony, Workshop Session")
                    schedule_desc = st.text_area("📝 Description", placeholder="Provide details about this activity...")
                    schedule_location = st.text_input("📍 Location (Optional)", placeholder="e.g., Main Hall, Room 101")
                    
                    col_btn1, col_btn2 = st.columns([1, 4])
                    with col_btn1:
                        submitted = st.form_submit_button("➕ Add", use_container_width=True)
                    
                    if submitted and schedule_title:
                        new_schedule = {
                            "id": str(uuid.uuid4()),
                            "datetime": f"{schedule_date} {schedule_time}",
                            "title": schedule_title,
                            "description": schedule_desc,
                            "location": schedule_location,
                            "added_by": st.session_state.user_name
                        }
                        
                        event["schedules"].append(new_schedule)
                        # Sort schedules by datetime
                        event["schedules"].sort(key=lambda x: x["datetime"])
                        st.success("✅ Schedule item added!")
                        time.sleep(0.5)
                        st.rerun()
        else:
            st.info("ℹ️ Only Admin and Core members can add schedule items.")
        
        st.divider()
        
        # Display schedule
        if not event["schedules"]:
            st.info("📭 No schedule items yet.")
        else:
            for idx, schedule in enumerate(event["schedules"]):
                st.markdown(f"""
                <div class="schedule-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #667eea;">📌 {schedule['title']}</h3>
                        <span style="background: #667eea; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">
                            🕐 {schedule['datetime']}
                        </span>
                    </div>
                    <p style="margin-top: 0.8rem; color: #2c3e50;">{schedule['description']}</p>
                    {f'<p style="margin-top: 0.5rem;"><strong>📍 Location:</strong> {schedule.get("location", "TBA")}</p>' if schedule.get("location") else ''}
                    <small style="color: #7f8c8d;">Added by: {schedule['added_by']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if idx < len(event["schedules"]) - 1:
                    st.write("")
    
    # Subevents Tab
    with tab3:
        st.header("🎪 Subevents")
        
        # Create subevent - Only Admin and Core can create
        if check_permission(event_id, user_role, ["admin", "core"]):
            with st.expander("➕ Create New Subevent", expanded=False):
                with st.form("create_subevent"):
                    subevent_name = st.text_input("🎪 Subevent Name", placeholder="e.g., AI Workshop, Networking Session")
                    subevent_desc = st.text_area("📝 Description", placeholder="Describe this subevent...")
                    subevent_capacity = st.number_input("👥 Max Participants (Optional)", min_value=0, value=0, step=1)
                    
                    col_btn1, col_btn2 = st.columns([1, 4])
                    with col_btn1:
                        submitted = st.form_submit_button("➕ Create", use_container_width=True)
                    
                    if submitted and subevent_name:
                        # Create subevent in database
                        result = db.create_subevent(
                            sub_event_name=subevent_name,
                            description=subevent_desc,
                            event_id=event_id,
                            venue_id=None
                        )
                        
                        if result["success"]:
                            # Update capacity if specified
                            if subevent_capacity > 0:
                                db.execute_query(
                                    "UPDATE Sub_events SET capacity = %s WHERE sub_event_id = %s",
                                    (subevent_capacity, result["sub_event_id"])
                                )
                            
                            st.success("✅ Subevent created!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
        else:
            st.info("ℹ️ Only Admin and Core members can create subevents.")
        
        st.divider()
        
        # Display subevents from database
        subevents = db.get_event_subevents(event_id)
        
        if not subevents:
            st.info("📭 No subevents created yet.")
        else:
            for subevent in subevents:
                subevent_id = subevent["sub_event_id"]
                subevent_name = subevent["sub_event_name"]
                
                # Check if user is registered (simplified - using session for now)
                # In production, create Subevent_Participants table
                is_registered = False  # Placeholder
                
                with st.expander(f"🎪 {subevent_name}", expanded=False):
                    col_sub1, col_sub2 = st.columns([3, 1])
                    
                    with col_sub1:
                        st.write(f"**Description:** {subevent['decription']}")  # Note: typo in schema
                        created_at = subevent.get('created_at', '')
                        if created_at:
                            timestamp = created_at.strftime('%Y-%m-%d') if hasattr(created_at, 'strftime') else str(created_at)[:10]
                            st.caption(f"Created on: {timestamp}")
                        
                        # Show capacity info if available
                        if subevent.get("capacity"):
                            st.write(f"👥 Capacity: {subevent['capacity']} participants")
                    
                    with col_sub2:
                        st.write("")
                        st.info("Join feature coming soon")
                    
                    st.divider()
                    
                    # Subevent chat
                    st.subheader("💬 Subevent Chat")
                    
                    # Chat input
                    with st.form(f"chat_form_{subevent_id}"):
                        col_chat1, col_chat2 = st.columns([5, 1])
                        with col_chat1:
                            message_text = st.text_input(
                                "Message", 
                                key=f"msg_input_{subevent_id}",
                                placeholder="Type your message...",
                                label_visibility="collapsed"
                            )
                        with col_chat2:
                            send_btn = st.form_submit_button("📤 Send", use_container_width=True)
                        
                        if send_btn and message_text:
                            # Send message to database
                            result = db.send_message(
                                event_id=event_id,
                                sender_username=st.session_state.user_email,
                                chat_message_text=message_text,
                                subevent_name=subevent_name,
                                idx_subevent_chat=1
                            )
                            
                            if result["success"]:
                                st.rerun()
                    
                    # Display messages from database
                    messages = db.get_subevent_chat(event_id, subevent_name, limit=10)
                    
                    if not messages:
                        st.info("No messages yet. Start the conversation!")
                    else:
                        for message in messages:
                            is_my_message = message["sender_username"] == st.session_state.user_email
                            timestamp = message['created_at'].strftime('%H:%M') if hasattr(message['created_at'], 'strftime') else str(message['created_at'])[11:16]
                            
                            if is_my_message:
                                col_space, col_msg = st.columns([1, 4])
                                with col_msg:
                                    st.markdown(f"""
                                    <div class="message-bubble my-message">
                                        <strong>You</strong><br>
                                        {message['chat_message_text']}<br>
                                        <small style="opacity: 0.8;">{timestamp}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                col_msg, col_space = st.columns([4, 1])
                                with col_msg:
                                    st.markdown(f"""
                                    <div class="message-bubble">
                                        <strong>{message['sender_username']}</strong><br>
                                        {message['chat_message_text']}<br>
                                        <small style="color: #7f8c8d;">{timestamp}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
    
    # Event Chat Tab
    with tab4:
        st.header("💬 Event Chat")
        st.caption("General discussion for all event participants")
        
        # Chat input
        with st.form("main_chat_form"):
            col_chat1, col_chat2 = st.columns([5, 1])
            with col_chat1:
                message_text = st.text_input(
                    "Message", 
                    key="main_chat_input",
                    placeholder="Type your message...",
                    label_visibility="collapsed"
                )
            with col_chat2:
                send_btn = st.form_submit_button("📤 Send", use_container_width=True)
            
            if send_btn and message_text:
                # Send message to database
                result = db.send_message(
                    event_id=event_id,
                    sender_username=st.session_state.user_email,
                    chat_message_text=message_text,
                    subevent_name="",  # Empty for main event chat
                    idx_event_chat=1
                )
                
                if result["success"]:
                    st.rerun()
        
        st.divider()
        
        # Display messages from database
        messages = db.get_event_chat(event_id, limit=20)
        
        if not messages:
            st.info("💬 No messages yet. Start the conversation!")
        else:
            for message in messages:
                is_my_message = message["sender_username"] == st.session_state.user_email
                timestamp = message['created_at'].strftime('%H:%M') if hasattr(message['created_at'], 'strftime') else str(message['created_at'])[11:16]
                
                if is_my_message:
                    col_space, col_msg = st.columns([1, 4])
                    with col_msg:
                        st.markdown(f"""
                        <div class="message-bubble my-message">
                            <strong>You</strong><br>
                            {message['chat_message_text']}<br>
                            <small style="opacity: 0.8;">{timestamp}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    col_msg, col_space = st.columns([4, 1])
                    with col_msg:
                        st.markdown(f"""
                        <div class="message-bubble">
                            <strong>{message['sender_username']}</strong><br>
                            {message['chat_message_text']}<br>
                            <small style="color: #7f8c8d;">{timestamp}</small>
                        </div>
                        """, unsafe_allow_html=True)
    
    # General Info Tab
    with tab5:
        st.header("ℹ️ General Information")
        
        # Note: General info editing would require adding a field to Eventz table
        # For now, just display event details
        
        st.divider()
        
        # Event Details Section
        st.subheader("📋 Event Details")
        
        col_detail1, col_detail2 = st.columns(2)
        with col_detail1:
            st.write(f"**🎫 Event Code:** `{event['event_code']}`")
            st.write(f"**📅 Start Date:** {event['start_date']}")
            st.write(f"**🕐 Start Time:** {event.get('start_time', 'TBA')}")
            st.write(f"**👤 Organizer:** {event.get('organiser_name', 'Unknown')}")
        
        with col_detail2:
            st.write(f"**🏷️ Status:** {event['event_status'].title()}")
            st.write(f"**📅 End Date:** {event['end_date']}")
            st.write(f"**🕐 End Time:** {event.get('end_time', 'TBA')}")
            st.write(f"**🎯 Event ID:** {event['event_id']}")
        
        st.divider()
        
        # Event Description
        st.subheader("📝 Description")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="font-size: 1.05rem; line-height: 1.6; color: #2c3e50;">{event['event_description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Category and Type
        st.divider()
        col_cat1, col_cat2 = st.columns(2)
        with col_cat1:
            st.metric("📂 Category", event.get('category', 'General'))
        with col_cat2:
            st.metric("🎭 Type", event.get('type_of_event', 'Conference'))

def main():
    """Main application logic"""
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    
    if "user_event_roles" not in st.session_state:
        st.session_state.user_event_roles = {}
    
    if "user_events" not in st.session_state:
        st.session_state.user_events = []
    
    # Database is initialized via @st.cache_resource decorator
    
    # Show appropriate page based on login status and current page
    if not st.session_state.logged_in:
        login_signup_page()
    else:
        load_custom_css()
        
        # Header with user info and logout
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%); 
                    padding: 2rem; 
                    border-radius: 20px; 
                    margin-bottom: 2rem; 
                    box-shadow: 0 10px 30px rgba(255, 107, 107, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 800;">🎯 Event Dashboard</h1>
                    <p style="margin: 0.5rem 0 0 0; color: rgba(255, 255, 255, 0.95); font-size: 1.1rem;">
                        Welcome back, <strong>{st.session_state.user_name}</strong>! 👋
                    </p>
                    <small style="color: rgba(255, 255, 255, 0.9); font-size: 0.95rem;">📧 {st.session_state.user_email}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        header_col1, header_col2, header_col3, header_col4 = st.columns([2, 1, 1, 1])
        
        with header_col1:
            st.markdown("<div style='padding-top: 0.5rem;'></div>", unsafe_allow_html=True)
        
        with header_col2:
            st.markdown("<div style='padding-top: 0.8rem;'></div>", unsafe_allow_html=True)
            db = init_database()
            my_events_count = len(db.get_user_events(st.session_state.user_id))
            st.metric("My Events", my_events_count)
        
        with header_col3:
            st.markdown("<div style='padding-top: 0.8rem;'></div>", unsafe_allow_html=True)
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "events"
                st.rerun()
        
        with header_col4:
            st.markdown("<div style='padding-top: 0.8rem;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.divider()
        
        # Show appropriate page
        if st.session_state.current_page == "events":
            events_page()
        elif st.session_state.current_page == "create_event":
            create_event_page()
        elif st.session_state.current_page == "event_details":
            event_details_page()

if __name__ == "__main__":
    main()
