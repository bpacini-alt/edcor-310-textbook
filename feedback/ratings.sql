-- Shared schema for the Bang for Buck ratings test.
-- The Worker also creates these objects automatically when the API is first used.
CREATE TABLE IF NOT EXISTS reading_ratings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book TEXT NOT NULL,
  reading_id TEXT NOT NULL,
  semester TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 4),
  comment TEXT NOT NULL DEFAULT '',
  improvement TEXT NOT NULL DEFAULT '',
  client_id TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (book, reading_id, semester, client_id)
);
CREATE INDEX IF NOT EXISTS idx_reading_ratings_lookup
  ON reading_ratings (book, reading_id, semester);
