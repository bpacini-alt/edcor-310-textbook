-- Shared schema for page ratings in both textbooks.
-- The Worker creates these objects automatically when the API is first used.
CREATE TABLE IF NOT EXISTS reading_ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book TEXT NOT NULL,
  reading_id TEXT NOT NULL,
  semester TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 4),
  comment TEXT NOT NULL DEFAULT '',
  improvement TEXT NOT NULL DEFAULT '',
  clarity_rating INTEGER CHECK (clarity_rating BETWEEN 1 AND 5),
  practice_rating INTEGER CHECK (practice_rating BETWEEN 1 AND 5),
  practice_na INTEGER NOT NULL DEFAULT 0 CHECK (practice_na IN (0, 1)),
  polish_rating INTEGER CHECK (polish_rating BETWEEN 1 AND 5),
  client_id TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (book, reading_id, semester, client_id)
);
CREATE INDEX IF NOT EXISTS idx_reading_ratings_lookup
  ON reading_ratings (book, reading_id, semester);
