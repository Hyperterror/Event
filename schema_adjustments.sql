-- Schema Adjustments for Event Contact System
-- Run these queries to adjust your database schema for the app

USE event;

-- 1. Change event_code from INT to VARCHAR to support codes like "TECH2024"
ALTER TABLE Eventz MODIFY event_code VARCHAR(50);

-- 2. Add role column to Joins table for event-specific roles
ALTER TABLE Joins ADD COLUMN user_role VARCHAR(20) DEFAULT 'participant';

-- 3. Create Subevent_Participants table to track subevent registrations
CREATE TABLE IF NOT EXISTS Subevent_Participants (
    user_id INT,
    sub_event_id INT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, sub_event_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (sub_event_id) REFERENCES Sub_events(sub_event_id) ON DELETE CASCADE
);

-- 4. Add email column to Users table (optional - if you want to use email for login)
-- ALTER TABLE Users ADD COLUMN email VARCHAR(200) UNIQUE;

-- 5. Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_event_status ON Eventz(event_status);
CREATE INDEX IF NOT EXISTS idx_event_code ON Eventz(event_code);
CREATE INDEX IF NOT EXISTS idx_username ON Users(username);
CREATE INDEX IF NOT EXISTS idx_event_id_chat ON Chat_Messages(event_id);
CREATE INDEX IF NOT EXISTS idx_subevent_name ON Chat_Messages(subevent_name);

-- 6. Add capacity column to Sub_events for participant limits
ALTER TABLE Sub_events ADD COLUMN capacity INT DEFAULT NULL;

-- 7. Verify changes
SHOW TABLES;
DESCRIBE Eventz;
DESCRIBE Joins;
DESCRIBE Subevent_Participants;

-- 8. Sample data for testing (optional)
-- INSERT INTO Users (first_name, last_name, mobile_no, username, rpassword, rrole)
-- VALUES ('Admin', 'User', '+1234567890', 'admin', SHA2('admin123', 256), 'admin');

SELECT 'Schema adjustments completed successfully!' AS Status;
