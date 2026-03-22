/*users*/
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE
);


/*events*/
CREATE TABLE Events (
    event_id INT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL, --  "Bestieversary"
    target_date DATE NOT NULL,
    event_type VARCHAR(50) -- e.g., 'birthday', 'trip'
);


/*memories*/
CREATE TABLE Memories (
    memory_id INT PRIMARY KEY,
    uploaded_by INT, -- Links back to the user_id who posted it
    media_url VARCHAR(500) NOT NULL,
    media_type VARCHAR(10) CHECK (media_type IN ('photo', 'video')),
    caption TEXT,
    memory_date DATE, -- The date the photo/video was actually taken
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
);