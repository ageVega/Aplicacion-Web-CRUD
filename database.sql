-- Crea primero la tabla houses
CREATE TABLE houses (
    id SERIAL PRIMARY KEY,
    house_name VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crea después la tabla tasks, puede dar error si no se crean por separado
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    priority INTEGER CHECK (priority >= 1 AND priority <= 5) NOT NULL,
    house_id INTEGER REFERENCES houses(id) ON DELETE CASCADE
);
