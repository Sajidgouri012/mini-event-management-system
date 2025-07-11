-- Create extension for UUID support (if not already present)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------
-- Table: events
-- -----------------------------
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    location TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0)
);

-- -----------------------------
-- Table: attendees
-- -----------------------------
CREATE TABLE attendees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT _event_email_uc UNIQUE (event_id, email)
);
