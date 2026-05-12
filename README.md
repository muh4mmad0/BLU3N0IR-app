# BLU3N0IR — Cyberpunk Calculator
### DBMS Project | Python + Flask + SQLite

```
  ██████╗ ██╗     ██╗   ██╗██████╗ ███╗   ██╗ ██████╗ ██╗██████╗
  ██╔══██╗██║     ██║   ██║╚════██╗████╗  ██║██╔═══██╗██║██╔══██╗
  ██████╔╝██║     ██║   ██║ █████╔╝██╔██╗ ██║██║   ██║██║██████╔╝
  ██╔══██╗██║     ██║   ██║ ╚═══██╗██║╚██╗██║██║   ██║██║██╔══██╗
  ██████╔╝███████╗╚██████╔╝██████╔╝██║ ╚████║╚██████╔╝██║██║  ██║
  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═╝
```

---

## Project Structure

```
BLU3N0IR/
├── app.py              ← Flask backend + API routes
├── database.py         ← SQLite CRUD operations
├── requirements.txt    ← Python dependencies
├── templates/
│   └── index.html      ← Full frontend (HTML + CSS + JS)
└── blu3noir.db         ← SQLite database (auto-created on run)
```

---

## Features

### 🔢 Calculator
- **Basic**: +, −, ×, ÷, %, parentheses
- **Scientific**: sin, cos, tan, sqrt, log, ln, exp, factorial, π, e, x^n
- Input validation via safe expression evaluator (no `eval` injection)
- Keyboard support (numbers, operators, Enter, Escape, Backspace)
- Ripple animations on button press

### 🗄️ Database (SQLite)
| Operation | SQL |
|-----------|-----|
| Store result | `INSERT INTO calculations` |
| View history | `SELECT ... ORDER BY id DESC` |
| Search | `SELECT ... WHERE expression LIKE ?` |
| Delete one | `DELETE WHERE id = ?` |
| Delete all | `DELETE FROM calculations` |

**Schema:**
```sql
CREATE TABLE calculations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT    NOT NULL,
    result     TEXT    NOT NULL,
    timestamp  TEXT    NOT NULL
);
```

### 📦 Export
- **CSV**: Download full history as spreadsheet
- **TXT**: Download formatted text report

---

## Setup & Run

```bash
# 1. Install dependencies
pip install flask

# 2. Run the app
python app.py

# 3. Open browser
http://127.0.0.1:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/calculate` | Evaluate expression, save to DB |
| GET | `/api/history` | Fetch recent history |
| GET | `/api/search?q=` | Search history |
| DELETE | `/api/delete/<id>` | Delete one record |
| DELETE | `/api/delete-all` | Clear all records |
| GET | `/api/export/csv` | Download CSV |
| GET | `/api/export/txt` | Download TXT |

---

## DBMS Concepts Demonstrated
- **DDL**: CREATE TABLE, CREATE INDEX
- **DML**: INSERT, SELECT, DELETE
- **Parameterized Queries**: Prevents SQL injection
- **Indexing**: `idx_timestamp` for fast ORDER BY
- **Aggregation**: Record counting
- **Pattern Matching**: LIKE operator for search

---

*BLU3N0IR — Where computation meets the cyberpunk aesthetic.*
