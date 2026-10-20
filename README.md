
# Study Notes Assistant MCP Server

## 1. Project Overview

The Study Notes Assistant is a Python-based Model Context Protocol (MCP) server that helps users organize and retrieve study notes. It uses SQLite to store notes and exposes tools, a resource, and a reusable prompt through MCP.

## 2. Technologies Used

- Python
- Model Context Protocol (MCP) Python SDK
- SQLite
- unittest
- MCP Inspector

## 3. Features

- Create study notes with a title, content, and topic tag.
- Search notes by title, content, or tag.
- List all unique tags.
- Read the saved notes catalogue through an MCP resource.
- Generate a reusable prompt for summarizing notes about a topic.
- Validate inputs and return clear errors for invalid values.

## 4. MCP Components

### Tools

| Tool | Description |
|---|---|
| `create_note` | Creates a study note. |
| `search_notes` | Searches notes by title, content, or tag. |
| `list_tags` | Lists unique topic tags. |

### Resource

- URI: `notes://catalogue`
- Purpose: Provides a catalogue of saved notes, including their IDs, titles, and tags.

### Prompt

- Name: `summarize_note`
- Purpose: Creates instructions for summarizing study notes related to a given topic.

## 5. Project Structure

```text
study-notes-assistant/
├── server.py
├── test_server.py
├── requirements.txt
├── README.md
├── .gitignore
└── study_notes.db  (generated locally)
```

## 6. Installation

Python 3.10 or later is recommended.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## 7. Run the Server

```powershell
python server.py
```

The server uses standard input/output (stdio) for MCP communication. Connect to it using an MCP-compatible client or MCP Inspector.

## 8. Run Automated Tests

```powershell
python -m unittest -v test_server.py
```

The project has five automated unit tests covering note creation, searching, tag listing, and invalid inputs.

## 9. Testing Evidence

The project was tested using MCP Inspector. The verified operations include:

- Creating a note successfully.
- Searching for matching notes.
- Listing available tags.
- Reading the notes catalogue resource.
- Retrieving the summarization prompt.

Screenshots of actual test results should be included in the project report.

## 10. Conclusion

The Study Notes Assistant demonstrates how an MCP server can expose useful tools, resources, and prompts to an AI application. SQLite provides local persistence, while automated tests help verify core functionality.
