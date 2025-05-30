CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)

CREATE TABLE user_question_bank (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    correct_attempts INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    consecutive_correct INTEGER DEFAULT 0,
    mastered BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE (user_id, question_id)
);

CREATE INDEX idx_user_question ON user_question_bank(user_id, question_id);
CREATE INDEX IF NOT EXISTS idx_uqb_user ON user_question_bank(user_id);
CREATE INDEX IF NOT EXISTS idx_uqb_mastered ON user_question_bank(user_id, mastered);
CREATE INDEX IF NOT EXISTS idx_uqb_question ON user_question_bank(question_id);
