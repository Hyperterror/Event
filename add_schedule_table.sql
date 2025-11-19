-- Add Schedule table for Event Contact System
-- Run this to add schedule functionality

USE event;

-- Create Schedule table
CREATE TABLE IF NOT EXISTS Event_Schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    schedule_date DATE NOT NULL,
    schedule_time TIME NOT NULL,
    location VARCHAR(255),
    added_by_user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES Eventz(event_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by_user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Add index for better performance
CREATE INDEX idx_event_schedule ON Event_Schedule(event_id);
CREATE INDEX idx_schedule_datetime ON Event_Schedule(schedule_date, schedule_time);

SELECT 'Schedule table created successfully!' AS Status;
