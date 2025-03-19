CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    site_name VARCHAR(255) NOT NULL,
    site_url VARCHAR(255),
    encrypted_password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
