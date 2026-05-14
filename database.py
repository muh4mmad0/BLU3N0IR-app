"""
BLU3N0IR — Database Layer
MySQL integration for calculation history
"""

import mysql.connector
from mysql.connector import pooling
import csv, io
from datetime import datetime

# ─── MySQL Config — edit these before running ─────────────────────────────────

DB_CONFIG = {
    "host":     "yamanote.proxy.rlwy.net",
    "port":     52909,
    "user":     "root",           # ← your MySQL username
    "password": "dyfAhoMpHoNNdcVLMAInINIfQPtBPbEy",  # ← your MySQL password
    "database": "railway",
}
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS calculations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expression VARCHAR(255),
    result VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

con.commit()

# ─── Schema ──────────────────────────────────────────────────────────────────s

CREATE_DB_SQL = "CREATE DATABASE IF NOT EXISTS blu3noir CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS calculations (
    id         INT          NOT NULL AUTO_INCREMENT,
    expression VARCHAR(500) NOT NULL,
    result     VARCHAR(200) NOT NULL,
    timestamp  DATETIME     NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_timestamp (timestamp DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

# ─── Connection Pool ──────────────────────────────────────────────────────────

_pool = None

def _get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="blu3noir_pool",
            pool_size=5,
            **DB_CONFIG
        )
    return _pool

def get_conn():
    """Get a connection from the pool."""
    return _get_pool().get_connection()

# ─── Init ─────────────────────────────────────────────────────────────────────

def init_db():
    # Step 1: create database if it doesn't exist (connect without db)
    cfg_no_db = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    tmp = mysql.connector.connect(**cfg_no_db)
    cur = tmp.cursor()
    cur.execute(CREATE_DB_SQL)
    cur.close()
    tmp.close()

    # Step 2: create table + index inside the database
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()

    print(f"  [DB] MySQL database initialized → {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

# ─── CRUD Operations ─────────────────────────────────────────────────────────

def save_calculation(expression: str, result: str):
    """INSERT a new calculation record."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calculations (expression, result, timestamp) VALUES (%s, %s, %s)",
        (expression, result, ts)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_history(limit: int = 50) -> list[dict]:
    """SELECT recent calculation history."""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, expression, result, timestamp FROM calculations ORDER BY id DESC LIMIT %s",
        (limit,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Convert datetime objects to string for JSON serialisation
    for r in rows:
        if isinstance(r.get('timestamp'), datetime):
            r['timestamp'] = r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return rows

def search_history(query: str) -> list[dict]:
    """SELECT records matching expression or result."""
    pattern = f"%{query}%"
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT id, expression, result, timestamp FROM calculations
           WHERE expression LIKE %s OR result LIKE %s
           ORDER BY id DESC LIMIT 100""",
        (pattern, pattern)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for r in rows:
        if isinstance(r.get('timestamp'), datetime):
            r['timestamp'] = r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return rows

def delete_record(record_id: int):
    """DELETE a specific record by ID."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM calculations WHERE id = %s", (record_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_all():
    """TRUNCATE the calculations table and reset AUTO_INCREMENT."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE calculations")
    conn.commit()
    cur.close()
    conn.close()

def export_csv() -> str:
    """Export all history as CSV string."""
    records = get_history(10000)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'expression', 'result', 'timestamp'])
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue()
