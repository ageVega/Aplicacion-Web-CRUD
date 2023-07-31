-- Crea primero la tabla houses
CREATE TABLE houses (
    id SERIAL PRIMARY KEY,
    house_name VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Crea después las tablas dependientes de houses, puede dar error si no se crean por separado
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    priority INTEGER CHECK (priority >= 1 AND priority <= 7) NOT NULL,
    house_id INTEGER REFERENCES houses(id) ON DELETE CASCADE
);

CREATE TABLE priority_levels (
    id SERIAL PRIMARY KEY,
    level INTEGER CHECK (level >= 1 AND level <= 7) NOT NULL,
    name VARCHAR(25) NOT NULL,
    house_id INTEGER REFERENCES houses(id) ON DELETE CASCADE
);
