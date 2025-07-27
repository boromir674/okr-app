CREATE TABLE IF NOT EXISTS objectives (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    progress INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS key_results (
    id SERIAL PRIMARY KEY,
    objective_id INT REFERENCES objectives(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    progress INT DEFAULT 0,
    metric VARCHAR(255)
);
