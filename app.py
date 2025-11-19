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

# Design System - CSS Custom Properties and Component Styles
def load_design_system():
    """Load the complete design system with CSS custom properties"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* ===== CSS CUSTOM PROPERTIES (DESIGN TOKENS) ===== */
    :root {
      /* Primary Brand Colors (Warm Coral-Orange-Yellow Spectrum) */
      --color-coral: #FF6B6B;
      --color-orange: #FFB84D;
      --color-yellow: #FFE66D;
      --color-teal: #4ECDC4;
      --color-mint: #95E1D3;
      --color-salmon: #FFA07A;
      
      /* Neutral Colors */
      --color-gray-900: #2D3142;
      --color-gray-700: #5A6175;
      --color-gray-500: #8B92A8;
      --color-gray-300: #E8EAED;
      --color-gray-100: #FAFBFC;
      --color-white: #FFFFFF;
      
      /* Gradients */
      --gradient-header: linear-gradient(135deg, #FF8C69 0%, #FFB84D 50%, #FFE66D 100%);
      --gradient-button: linear-gradient(135deg, #FF6B6B 0%, #FFB84D 100%);
      --gradient-card-a: linear-gradient(135deg, #FF9A76 0%, #FFAD87 100%);
      --gradient-card-b: linear-gradient(135deg, #FFB84D 0%, #FFCF5C 100%);
      --gradient-card-c: linear-gradient(135deg, #FFE66D 0%, #FFF09E 100%);
      
      /* Spacing Scale (4px baseline grid) */
      --space-xs: 4px;
      --space-sm: 8px;
      --space-md: 12px;
      --space-lg: 16px;
      --space-xl: 24px;
      --space-2xl: 32px;
      --space-3xl: 48px;
      --space-4xl: 64px;
      
      /* Typography */
      --font-family: 'Inter', 'Segoe UI', -apple-system, system-ui, sans-serif;
      
      /* Shadows */
      --shadow-xs: 0 1px 2px rgba(45, 49, 66, 0.04);
      --shadow-sm: 0 2px 8px rgba(45, 49, 66, 0.06);
      --shadow-md: 0 4px 16px rgba(45, 49, 66, 0.08);
      --shadow-lg: 0 8px 24px rgba(45, 49, 66, 0.12);
      --shadow-xl: 0 16px 48px rgba(45, 49, 66, 0.16);
      
      /* Border Radius */
      --radius-sm: 6px;
      --radius-md: 8px;
      --radius-lg: 12px;
      --radius-xl: 16px;
      --radius-2xl: 24px;
      --radius-full: 9999px;
      
      /* Transitions */
      --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
      --duration-fast: 200ms;
      --duration-normal: 300ms;
    }
    
    /* ===== GLOBAL STYLES ===== */
    html, body, [class*="css"] {
        font-family: var(--font-family);
        background-color: var(--color-gray-100);
    }
    
    .main {
        padding: 2rem;
        background-color: var(--color-gray-100);
    }
    
    .stApp {
        background-color: var(--color-gray-100);
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1 {
        font-size: 32px;
        line-height: 40px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: var(--color-gray-900);
        margin: 0;
        font-family: var(--font-family);
    }
    
    h2 {
        font-size: 24px;
        line-height: 32px;
        font-weight: 600;
        letter-spacing: -0.3px;
        color: var(--color-gray-900);
        margin: 0;
        font-family: var(--font-family);
    }
    
    h3 {
        font-size: 20px;
        line-height: 28px;
        font-weight: 600;
        letter-spacing: -0.2px;
        color: var(--color-gray-900);
        margin: 0;
        font-family: var(--font-family);
    }
    
    h4 {
        font-size: 16px;
        line-height: 24px;
        font-weight: 600;
        color: var(--color-gray-900);
        margin: 0;
        font-family: var(--font-family);
    }
    
    p {
        font-size: 14px;
        line-height: 22px;
        font-weight: 400;
        color: var(--color-gray-700);
    }
    
    a {
        color: var(--color-coral);
        text-decoration: none;
        transition: color var(--duration-fast) ease;
    }
    
    a:hover {
        color: #FF5252;
        text-decoration: underline;
    }
    
    /* ===== BUTTON COMPONENTS ===== */
    /* Primary Button (Default) */
    .stButton>button {
        background: var(--gradient-button);
        color: var(--color-white);
        padding: 12px 24px;
        border-radius: var(--radius-md);
        font-size: 14px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
        transition: all var(--duration-normal) var(--ease-standard);
        font-family: var(--font-family);
    }
    
    .stButton>button:hover {
        filter: brightness(1.1);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        transform: translateY(-1px);
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    .stButton>button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        box-shadow: none;
    }
    
    /* Secondary Button */
    .stButton.secondary>button {
        background: var(--color-white);
        color: var(--color-gray-900);
        border: 2px solid var(--color-gray-300);
        box-shadow: none;
    }
    
    .stButton.secondary>button:hover {
        background: rgba(255, 184, 77, 0.1);
        border-color: var(--color-orange);
        filter: none;
        box-shadow: none;
    }
    
    /* Icon Button */
    .stButton.icon>button {
        width: 40px;
        height: 40px;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-white);
        color: var(--color-gray-900);
        border: 1px solid var(--color-gray-300);
        box-shadow: none;
    }
    
    .stButton.icon>button:hover {
        background: rgba(255, 184, 77, 0.1);
        border-color: var(--color-orange);
        filter: none;
    }
    
    /* ===== ROLE BADGE COMPONENTS ===== */
    .role-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: var(--radius-full);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--color-white);
        letter-spacing: 0.3px;
    }
    
    .admin-badge {
        background: var(--color-coral);
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
    }
    
    .core-badge {
        background: var(--color-orange);
        box-shadow: 0 2px 8px rgba(255, 184, 77, 0.3);
    }
    
    .participant-badge {
        background: var(--color-teal);
        box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
    }
    
    /* ===== STATUS BADGE COMPONENTS ===== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: var(--radius-full);
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    .status-badge--ongoing {
        background: rgba(78, 205, 196, 0.15);
        color: #2D7873;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    .status-badge--upcoming {
        background: rgba(255, 160, 122, 0.15);
        color: #B8563D;
        border: 1px solid rgba(255, 160, 122, 0.3);
    }
    
    .status-badge--completed {
        background: rgba(255, 107, 107, 0.15);
        color: #B84A4A;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    
    /* ===== INPUT FIELD COMPONENTS ===== */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        height: 44px;
        padding: 12px 16px;
        border: 2px solid var(--color-gray-300);
        border-radius: var(--radius-md);
        background: var(--color-white);
        font-size: 14px;
        color: var(--color-gray-900);
        transition: all var(--duration-fast) ease;
        font-family: var(--font-family);
    }
    
    .stTextArea>div>div>textarea {
        min-height: 120px;
        height: auto;
        resize: vertical;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: var(--color-gray-500);
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        outline: none;
        border-color: var(--color-coral);
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.15);
    }
    
    .stTextInput>div>div>input:disabled,
    .stTextArea>div>div>textarea:disabled {
        background: var(--color-gray-100);
        color: var(--color-gray-500);
        cursor: not-allowed;
    }
    
    /* Select Dropdown */
    .stSelectbox>div>div>select {
        height: 44px;
        padding: 12px 16px;
        border: 2px solid var(--color-gray-300);
        border-radius: var(--radius-md);
        background: var(--color-white);
        font-size: 14px;
        color: var(--color-gray-900);
        cursor: pointer;
        transition: all var(--duration-fast) ease;
        font-family: var(--font-family);
    }
    
    .stSelectbox>div>div>select:focus {
        outline: none;
        border-color: var(--color-coral);
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.15);
    }
    
    /* ===== MESSAGE BUBBLE COMPONENTS ===== */
    .message-bubble {
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 70%;
        margin: 8px 0;
        font-size: 14px;
        line-height: 22px;
    }
    
    .message-bubble--sent {
        background: var(--gradient-button);
        color: var(--color-white);
        border-radius: 16px 16px 4px 16px;
        align-self: flex-end;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.2);
        margin-left: 30%;
    }
    
    .message-bubble--received {
        background: var(--color-white);
        color: var(--color-gray-900);
        border: 1px solid var(--color-gray-300);
        border-radius: 16px 16px 16px 4px;
        align-self: flex-start;
        box-shadow: 0 1px 4px rgba(45, 49, 66, 0.04);
        margin-right: 30%;
    }
    
    .message-bubble__time {
        font-size: 11px;
        margin-top: 4px;
        opacity: 0.8;
    }
    
    /* ===== HEADER COMPONENT ===== */
    .app-header {
        background: var(--gradient-header);
        padding: var(--space-2xl) var(--space-3xl);
        border-radius: 0 0 var(--radius-2xl) var(--radius-2xl);
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.15);
        margin-bottom: var(--space-2xl);
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: var(--space-lg);
    }
    
    .header-icon {
        width: 48px;
        height: 48px;
        background: rgba(255, 255, 255, 0.25);
        border-radius: var(--radius-lg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
    
    .header-title {
        font-size: 32px;
        font-weight: 700;
        color: var(--color-white);
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0;
    }
    
    .header-right {
        text-align: right;
    }
    
    .header-greeting {
        font-size: 16px;
        font-weight: 600;
        color: var(--color-white);
        margin-bottom: 4px;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-email {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
    }
    
    @media (max-width: 640px) {
        .app-header {
            padding: var(--space-xl) 20px;
        }
        
        .header-content {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--space-lg);
        }
        
        .header-title {
            font-size: 28px;
        }
        
        .header-right {
            text-align: left;
        }
    }
    
    /* ===== ANNOUNCEMENT COMPONENT ===== */
    .announcement-box {
        background: var(--color-white);
        border-left: 4px solid var(--color-orange);
        border-radius: var(--radius-md);
        padding: 20px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 16px;
    }
    
    .announcement-box__header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    
    .announcement-box__body {
        font-size: 14px;
        line-height: 22px;
        color: var(--color-gray-900);
        margin-bottom: 12px;
    }
    
    /* ===== SCHEDULE ITEM COMPONENT ===== */
    .schedule-item {
        background: var(--color-white);
        border-left: 5px solid var(--color-orange);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: all var(--duration-normal) ease;
    }
    
    .schedule-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(255, 184, 77, 0.15);
    }
    
    .schedule-item__title {
        font-size: 20px;
        font-weight: 600;
        color: var(--color-orange);
        margin: 0 0 8px 0;
    }
    
    /* ===== EVENT CARD COMPONENT ===== */
    .event-card {
        background: var(--color-white);
        border-radius: var(--radius-xl);
        padding: var(--space-xl);
        box-shadow: var(--shadow-sm);
        transition: all var(--duration-normal) var(--ease-standard);
        position: relative;
        overflow: hidden;
        margin: var(--space-xl) 0;
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        transition: height var(--duration-normal) ease;
    }
    
    .event-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .event-card--ongoing::before {
        background: linear-gradient(90deg, #4ECDC4, #95E1D3);
    }
    
    .event-card--upcoming::before {
        background: linear-gradient(90deg, #FFA07A, #FFCDB3);
    }
    
    .event-card--completed::before {
        background: linear-gradient(90deg, #FF6B6B, #FFB3B3);
    }
    
    /* ===== TAB STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--color-white);
        border-bottom: 2px solid var(--color-gray-300);
        padding: 0 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 16px 20px;
        font-size: 14px;
        font-weight: 500;
        color: var(--color-gray-700);
        border-bottom: 3px solid transparent;
        cursor: pointer;
        transition: all var(--duration-fast) ease;
        position: relative;
        bottom: -2px;
        background: transparent;
        border-top: none;
        border-left: none;
        border-right: none;
        font-family: var(--font-family);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-gray-900);
        background: rgba(255, 184, 77, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--color-coral);
        border-bottom-color: var(--color-coral);
        font-weight: 600;
    }
    
    /* ===== METRIC STYLING ===== */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
        font-family: var(--font-family);
        color: var(--color-gray-900);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        font-family: var(--font-family);
        color: var(--color-gray-700);
    }
    
    /* ===== ALERT/MESSAGE STYLING ===== */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: var(--radius-lg);
        padding: 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        font-family: var(--font-family);
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--color-gray-100);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-button);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFB84D 0%, #FF6B6B 100%);
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 640px) {
        h1 { font-size: 28px; line-height: 36px; }
        h2 { font-size: 22px; line-height: 30px; }
        .stButton>button { padding: 10px 20px; font-size: 13px; }
        .main { padding: 1rem; }
    }
    
    /* ===== REDUCED MOTION SUPPORT ===== */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* ===== FOCUS INDICATORS (ACCESSIBILITY) ===== */
    :focus-visible {
        outline: 2px solid var(--color-coral);
        outline-offset: 2px;
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

def get_status_badge(status):
    """Return HTML for status badge with icon"""
    status_config = {
        "ongoing": {
            "class": "status-badge--ongoing",
            "icon": "🟢",
            "text": "LIVE"
        },
        "upcoming": {
            "class": "status-badge--upcoming",
            "icon": "🟡",
            "text": "UPCOMING"
        },
        "completed": {
            "class": "status-badge--completed",
            "icon": "🔴",
            "text": "COMPLETED"
        }
    }
    
    config = status_config.get(status.lower(), status_config["upcoming"])
    return f'<span class="status-badge {config["class"]}">{config["icon"]} {config["text"]}</span>'

def render_header(user_name, user_email):
    """Render the application header with gradient background"""
    header_html = f"""
    <div class="app-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">🎯</div>
          <h1 class="header-title">Event Dashboard</h1>
        </div>
        <div class="header-right">
          <div class="header-greeting">Welcome back, {user_name}! 👋</div>
          <div class="header-email">📧 {user_email}</div>
        </div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def check_permission(event_id, user_role, required_roles):
    """Check if user has permission based on role"""
    return user_role.lower() in [r.lower() for r in required_roles]

def login_signup_page():
    load_design_system()
    
    # Custom CSS for login/register forms - Warm light theme
    st.markdown("""
    <style>
    /* Remove extra borders and clean up input fields */
    .stTextInput > div > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div > input {
        background: #FFFFFF !important;
        border: 2px solid #FFB84D !important;
        border-radius: 12px !important;
        padding: 0.9rem 1rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        color: #2D3142 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B6B !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.15) !important;
        background: #FFFFFF !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8B92A8 !important;
    }
    
    /* Label styling */
    .stTextInput > label {
        font-weight: 600 !important;
        color: #2D3142 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Form container - white with warm shadow */
    [data-testid="stForm"] {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #FFE6D9;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.1);
    }
    
    /* Login/Register page specific */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    
    /* Submit button in forms */
    [data-testid="stForm"] button[kind="primary"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFB84D 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    [data-testid="stForm"] button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.4) !important;
        filter: brightness(1.05) !important;
    }
    
    /* Page title */
    .login-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #FFB84D 50%, #FFE66D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: #5A6175;
        font-size: 1.1rem;
        text-align: center;
        font-weight: 500;
    }
    
    /* Tab styling for warm theme */
    .stTabs [data-baseweb="tab"] {
        color: #5A6175 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #FF6B6B !important;
    }
    
    /* Subheader styling */
    h3 {
        color: #1A1D2E !important;
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
            st.markdown("<h3 style='color: #1A1D2E; font-weight: 600; margin-bottom: 1.5rem;'>Welcome Back! 👋</h3>", unsafe_allow_html=True)
            
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
            st.markdown("<h3 style='color: #1A1D2E; font-weight: 600; margin-bottom: 1.5rem;'>Create Your Account ✨</h3>", unsafe_allow_html=True)
            
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
    load_design_system()
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.current_page = "events"
            st.rerun()
    
    st.title("➕ Create New Event")
    st.markdown("<p style='color: #5A6175;'>Fill in the details to create your event</p>", unsafe_allow_html=True)
    
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
    load_design_system()
    
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
        <div style="text-align: center; padding: 3rem; background: #FFF8F3; border-radius: 15px; margin: 2rem 0; border: 2px solid #FFE6D9;">
            <h2 style="color: #5A6175;">📭 No Events Available</h2>
            <p style="color: #8B92A8; font-size: 1.1rem;">There are no events to display at the moment.</p>
            <p style="color: #8B92A8;">Create a new event or join an existing one using an event code!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display event cards
    for event in events:
        event_id = event["event_id"]
        
        # Check if user is part of this event
        is_member = db.check_user_joined_event(st.session_state.user_id, event_id)
        
        # Get user role for this event
        user_role = "participant"
        if is_member:
            role_query = "SELECT user_role FROM joins WHERE user_id = %s AND event_id = %s"
            role_result = db.fetch_query(role_query, (st.session_state.user_id, event_id))
            if role_result:
                user_role = role_result[0].get("user_role", "participant")
        
        # Get counts from database
        announcements_count = len(db.get_event_announcements(event_id))
        subevents_count = len(db.get_event_subevents(event_id))
        messages_count = len(db.get_event_chat(event_id, limit=1000))
        
        # Determine status class for accent bar
        status_class = f"event-card--{event['event_status']}"
        
        # Create event card with proper HTML structure and CSS classes
        st.markdown(f'<div class="event-card {status_class}">', unsafe_allow_html=True)
        
        with st.container():
            # Event card header with title and badges
            col_header1, col_header2 = st.columns([3, 1])
            with col_header1:
                st.markdown(f"### 🎯 {event['title']}")
                if is_member:
                    st.markdown(get_role_badge(user_role), unsafe_allow_html=True)
            with col_header2:
                st.markdown(get_status_badge(event['event_status']), unsafe_allow_html=True)
            
            # Event details
            st.markdown(f"**Description:** {event['event_description']}")
            st.markdown(f"📅 **{event['start_date']}** to **{event['end_date']}**")
            st.markdown(f"🎫 Event Code: `{event['event_code']}`")
            
            st.divider()
            
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

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
    
    # Fetch related data
    announcements = db.get_event_announcements(event_id)
    
    # Get schedules (with fallback for cached instances)
    try:
        schedules = db.get_event_schedules(event_id)
    except AttributeError:
        st.warning("⚠️ Schedule feature requires app restart. Please refresh the page or clear cache (press 'C' then 'Clear cache').")
        schedules = []
    
    subevents = db.get_event_subevents(event_id
    
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
                            <small style="color: #8B92A8;">🕒 {timestamp}</small>
                        </div>
                        <p style="margin-top: 0.8rem; font-size: 1.05rem;">{announcement['announcement_text']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if announcement.get('file_name'):
                        st.info(f"📎 Attachment: **{announcement['file_name']}**")
                    
                    st.write("")
    
    # Schedule Tab
    with tab2:
        st.header("📅 Event Schedule")
        
        # Add schedule item - Only Admin and Core can add
        if check_permission(event_id, user_role, ["admin", "core"]):
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
                        result = db.add_schedule(
                            event_id=event_id,
                            title=schedule_title,
                            description=schedule_desc,
                            schedule_date=schedule_date,
                            schedule_time=schedule_time,
                            location=schedule_location,
                            added_by_user_id=st.session_state.user_id
                        )
                        
                        if result["success"]:
                            st.success("✅ Schedule item added!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"❌ Error adding schedule: {result['error']}")
        else:
            st.info("ℹ️ Only Admin and Core members can add schedule items.")
        
        st.divider()
        
        # Display schedule
        if not schedules:
            st.info("📭 No schedule items yet.")
        else:
            for idx, schedule in enumerate(schedules):
                st.markdown(f"""
                <div class="schedule-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #FFB84D;">📌 {schedule['title']}</h3>
                        <span style="background: linear-gradient(135deg, #FF6B6B 0%, #FFB84D 100%); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">
                            🕐 {schedule['datetime']}
                        </span>
                    </div>
                    <p style="margin-top: 0.8rem; color: #2D3142;">{schedule['description']}</p>
                    {f'<p style="margin-top: 0.5rem;"><strong>📍 Location:</strong> {schedule.get("location", "TBA")}</p>' if schedule.get("location") else ''}
                    <small style="color: #8B92A8;">Added by: {schedule['added_by']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if idx < len(schedules) - 1:
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
                                    <div class="message-bubble message-bubble--sent">
                                        <strong>You</strong><br>
                                        {message['chat_message_text']}<br>
                                        <div class="message-bubble__time">{timestamp}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                col_msg, col_space = st.columns([4, 1])
                                with col_msg:
                                    st.markdown(f"""
                                    <div class="message-bubble message-bubble--received">
                                        <strong>{message['sender_username']}</strong><br>
                                        {message['chat_message_text']}<br>
                                        <div class="message-bubble__time">{timestamp}</div>
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
                        <div class="message-bubble message-bubble--sent">
                            <strong>You</strong><br>
                            {message['chat_message_text']}<br>
                            <div class="message-bubble__time">{timestamp}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    col_msg, col_space = st.columns([4, 1])
                    with col_msg:
                        st.markdown(f"""
                        <div class="message-bubble message-bubble--received">
                            <strong>{message['sender_username']}</strong><br>
                            {message['chat_message_text']}<br>
                            <div class="message-bubble__time">{timestamp}</div>
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
        <div style="background: #FFF8F3; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FFB84D;">
            <p style="font-size: 1.05rem; line-height: 1.6; color: #2D3142;">{event['event_description']}</p>
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
        load_design_system()
        
        # Header with user info and logout
        render_header(st.session_state.user_name, st.session_state.user_email)
        
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
