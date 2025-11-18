# 🎯 Event Contact System

A comprehensive event management system built with Streamlit, featuring role-based access control, real-time messaging, and beautiful UI.

## ✨ Features

### 🔐 User Authentication
- **Registration**: Users register with name, email, and contact number
- **Login**: Secure login with email and password
- **Profile Management**: View user information in the header

### 🎫 Event Management
- **Create Events**: Admins can create events with unique event codes
- **Join Events**: Users join events using event codes and select their role (Admin/Core/Participant)
- **Event Dashboard**: View all events filtered by status (Ongoing/Upcoming/Completed) or "My Events"
- **Event Details**: Comprehensive event view with multiple tabs

### 👥 Role-Based Access Control
Three user roles with different permissions:

#### 🔴 Admin
- Full access to all features
- Create and manage events
- Post announcements
- Add schedule items
- Create subevents
- Edit general information
- Access all chats

#### 🔵 Core
- Post announcements
- Add schedule items
- Create subevents
- Edit general information
- Access all chats

#### 🟢 Participant
- View announcements
- View schedule
- Join subevents
- Access subevent chats (only if registered)
- Participate in event chat

### 📢 Announcements
- Admin and Core members can post announcements
- Support for file attachments (images, PDFs, documents)
- Timestamped with author information
- Role badges displayed

### 📅 Schedule Management
- Admin and Core can add schedule items
- Date, time, and location tracking
- Activity descriptions
- Sorted chronologically
- Beautiful card-based display

### 🎪 Subevents
- Admin and Core can create subevents
- Capacity management (optional)
- Participant registration system
- Dedicated chat for each subevent
- Only registered participants can access subevent chat

### 💬 Messaging
- **Event Chat**: General discussion for all event participants
- **Subevent Chat**: Private chat for registered subevent participants
- Real-time message display
- Role badges on messages
- Timestamped messages

### ℹ️ General Information
- Event details and information
- Admin and Core can edit
- Display event metadata (code, dates, organizer, status)

### 🎨 Enhanced UI
- Modern gradient cards for events
- Color-coded status indicators (🟢 Ongoing, 🟡 Upcoming, 🔴 Completed)
- Role badges with distinct colors
- Message bubbles with sender distinction
- Responsive layout
- Custom CSS styling
- Smooth transitions and hover effects

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL database (optional, currently using in-memory storage)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd event-contact-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create `.env` file):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
```

4. Run the application:
```bash
streamlit run app.py
```

## 📱 Usage Flow

1. **Register/Login**: Create an account or login with existing credentials
2. **Join Event**: Use the "Join Event" button and enter event code + select role
3. **Browse Events**: View all events or filter by status/your events
4. **Open Event**: Click "Open" to view event details
5. **Interact**: 
   - View announcements
   - Check schedule
   - Join subevents
   - Chat with participants
   - View general information

## 🗄️ Database Integration

The application is ready for MySQL integration. Uncomment the database code in:
- `database.py`: Database connection
- `app.py`: SQL queries for user authentication and data storage

### Database Schema (Suggested)

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contact VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    event_id VARCHAR(100) PRIMARY KEY,
    event_code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('upcoming', 'ongoing', 'completed'),
    organizer VARCHAR(255),
    general_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User-Event relationships
CREATE TABLE user_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    event_id VARCHAR(100),
    role ENUM('admin', 'core', 'participant'),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_email) REFERENCES users(email),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Additional tables for announcements, schedules, subevents, messages, etc.
```

## 🎨 Customization

### Colors
Edit the CSS in `load_custom_css()` function to change:
- Event card gradients
- Role badge colors
- Message bubble styles
- Button styles

### Roles
Modify role permissions in `check_permission()` function.

## 📝 Sample Events

The application includes 3 sample events:
1. **Tech Conference 2024** (Upcoming) - Code: TECH2024
2. **Music Festival** (Ongoing) - Code: MUSIC2024
3. **Sports Championship** (Completed) - Code: SPORTS2023

## 🔒 Security Notes

- Passwords are currently stored in plain text (for demo purposes)
- Implement proper password hashing (bcrypt, argon2) for production
- Add input validation and sanitization
- Implement CSRF protection
- Use environment variables for sensitive data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Known Issues

- File uploads are not persisted (frontend-only demo)
- No email verification
- Session state is cleared on page refresh
- No database persistence (currently in-memory)

## 🔮 Future Enhancements

- [ ] Email notifications
- [ ] File upload to cloud storage
- [ ] Export event data
- [ ] Calendar integration
- [ ] Mobile app
- [ ] Video conferencing integration
- [ ] Attendance tracking
- [ ] Event analytics dashboard
- [ ] Multi-language support

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ using Streamlit
