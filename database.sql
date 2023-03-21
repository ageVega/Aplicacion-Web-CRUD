-- Crea la tabla users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crea la tabla tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    priority INTEGER CHECK (priority >= 1 AND priority <= 5) NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
