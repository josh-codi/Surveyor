CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER IF NOT EXISTS [user_updated_at]
AFTER
UPDATE ON user FOR EACH ROW BEGIN
UPDATE user
SET updated_at = CURRENT_TIMESTAMP
WHERE id = old.id;
END;
-- 
-- 
-- 
CREATE TABLE IF NOT EXISTS survey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    admin_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES user(id)
);
CREATE TRIGGER IF NOT EXISTS [survey_updated_at]
AFTER
UPDATE ON survey FOR EACH ROW BEGIN
UPDATE survey
SET updated_at = CURRENT_TIMESTAMP
WHERE id = old.id;
END;
-- 
-- 
--
CREATE TABLE IF NOT EXISTS survey_field (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER,
    label TEXT NOT NULL,
    input_type TEXT NOT NULL,
    options TEXT NOT NULL DEFAULT '{}',
    position INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (survey_id) REFERENCES survey(id)
);
CREATE TRIGGER IF NOT EXISTS [survey_field_updated_at]
AFTER
UPDATE ON survey_field FOR EACH ROW BEGIN
UPDATE survey_field
SET updated_at = CURRENT_TIMESTAMP
WHERE id = old.id;
END;
--
--
--
CREATE TABLE IF NOT EXISTS survey_submission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES survey(id)
);
--
--
--
CREATE TABLE IF NOT EXISTS survey_submission_answer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_submission_id INTEGER NOT NULL,
    survey_field_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (survey_submission_id) REFERENCES survey_submission(id)
);