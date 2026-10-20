
import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Study Notes Assistant")

# Store the database in the project folder
DB_PATH = Path(__file__).parent / "study_notes.db"


def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """Create the notes table if it does not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tag TEXT NOT NULL
            )
        """)


@mcp.tool()
def create_note(title: str, content: str, tag: str) -> str:
    """Create a study note with a title, content, and topic tag."""
    title = title.strip()
    content = content.strip()
    tag = tag.strip()

    if not title or not content or not tag:
        raise ValueError("Title, content, and tag are required.")

    if len(title) > 100:
        raise ValueError("Title must not exceed 100 characters.")

    if len(content) > 10000:
        raise ValueError("Content must not exceed 10000 characters.")

    if len(tag) > 50:
        raise ValueError("Tag must not exceed 50 characters.")

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO notes (title, content, tag) VALUES (?, ?, ?)",
            (title, content, tag)
        )
        note_id = cursor.lastrowid

    return f"Note created successfully. ID: {note_id}, Title: {title}"


@mcp.tool()
def search_notes(keyword: str) -> str:
    """Search study notes by title, content, or tag."""
    keyword = keyword.strip()

    if not keyword:
        raise ValueError("Search keyword cannot be empty.")

    with get_connection() as conn:
        rows = conn.execute(
            """SELECT id, title, content, tag FROM notes
               WHERE title LIKE ? OR content LIKE ? OR tag LIKE ?
               ORDER BY id DESC LIMIT 20""",
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        ).fetchall()

    if not rows:
        return "No matching notes found."

    return "\n\n".join(
        f"ID: {row['id']}\nTitle: {row['title']}\n"
        f"Tag: {row['tag']}\nContent: {row['content']}"
        for row in rows
    )


@mcp.tool()
def list_tags() -> str:
    """List all unique topic tags used in study notes."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT tag FROM notes ORDER BY tag"
        ).fetchall()

    if not rows:
        return "No tags available yet."

    return "Available tags: " + ", ".join(row["tag"] for row in rows)


@mcp.resource("notes://catalogue")
def notes_catalogue() -> str:
    """Provide a catalogue of saved study notes."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, tag FROM notes ORDER BY id DESC"
        ).fetchall()

    if not rows:
        return "The study notes catalogue is empty."

    return "\n".join(
        f"ID: {row['id']} | Title: {row['title']} | Tag: {row['tag']}"
        for row in rows
    )


@mcp.prompt()
def summarize_note(topic: str) -> str:
    """Create a reusable prompt for summarizing notes about a topic."""
    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    return (
        f"Find study notes related to '{topic}'. "
        "Summarize the key concepts in simple language. "
        "Use bullet points and include important definitions. "
        "If no relevant notes exist, say so clearly."
    )


if __name__ == "__main__":
    initialize_database()
    print("Study Notes Assistant MCP server is starting...")
    mcp.run()
