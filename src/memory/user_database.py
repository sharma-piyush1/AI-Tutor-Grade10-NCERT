"""
User database - SQLite Integration
Handles user data storage and retrieval using SQLite.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent  # Go up to project root
DB_PATH = PROJECT_ROOT / "data" / "users.db"

class UserDatabase:
    """Manages user data storage and retrieval using SQLite."""

    def __init__(self):
        # Ensure data directory exists
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = str(DB_PATH)
        self._create_tables()
    
    def _create_tables(self):
        """Creates necessary tables in the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # User table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                last_active TEXT NOT NULL    
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, username):
        """Creates a new user in the database or returns existing user_id."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        try:
            cursor.execute("""
                INSERT INTO users (username, created_at, last_active)
                VALUES (?, ?, ?)
            """, (username, now, now))
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # User already exists, fetch user_id
            cursor.execute("""
                SELECT user_id FROM users WHERE username = ?
            """, (username,))
            user_id = cursor.fetchone()[0]
            # Update last_active
            cursor.execute("""
                UPDATE users SET last_active = ? WHERE user_id = ?
            """, (now, user_id))
        
        conn.commit()   
        conn.close()
        return user_id
    
    def save_message(self, user_id, role, content):
        """Save a single message to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO conversations (user_id, timestamp, role, content)
            VALUES (?, ?, ?, ?)
        """, (user_id, now, role, content))

        conn.commit()
        conn.close()

    def get_user_history(self, user_id, limit=50):
        """Retrieve conversation history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT role, content FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        # Return messages in chronological order
        return [{"role": row[0], "content": row[1]} for row in reversed(rows)]
    
    def clear_user_history(self, user_id):
        """Clear conversation history for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM conversations WHERE user_id = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    def get_user_stats(self, user_id):
        """Retrieve user statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM conversations WHERE user_id = ?
        """, (user_id,))

        count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT created_at, last_active FROM users WHERE user_id = ?
        """, (user_id,))
        
        user_data = cursor.fetchone()
        conn.close()

        return {
            "total_messages": count or 0,
            "created_at": user_data[0] if user_data else None,
            "last_active": user_data[1] if user_data else None
        }
    
    def export_conversation(self, user_id, format="txt"):
        """Export conversation history in specified format (txt or json)."""
        history = self.get_user_history(user_id, limit=1000)

        if format == "json":
            return json.dumps(history, indent=4)
        else:  # default to txt
            output = "AI TUTOR - CONVERSATION HISTORY\n"
            output += "=" * 60 + "\n\n"
            
            for msg in history:
                role = "Student" if msg["role"] == "user" else "AI Tutor"
                output += f"{role}: {msg['content']}\n\n"
            
            return output