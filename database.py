"""
BLU3N0IR — Database Layer (FIXED)
MySQL + Connection Pool (Render safe)
"""

import mysql.connector
from mysql.connector import pooling
from datetime import datetime
import csv
import io

# ─── DB CONFIG ─────────────────────────────────────────────

DB_CONFIG = {
    "host": "yamanote.proxy.rlwy.net",
    "port": 52909,
    "user": "root",
    "password": "dyfAhoMpHoNNdcVLMAInINIfQPtBPbEy",
    "database": "railway",
}

# ─── CONNECTION POOL ───────────────────────────────────────

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
    return _get_pool().get_connection()

# ─── INIT DB ───────────────────────────────────────────────

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS calculations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expression VARCHAR(500) NOT NULL,
    result VARCHAR(200) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def init_db():
    """Initialize database + table"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()
    print("[DB] Initialized successfully")

# ─── CRUD OPERATIONS ───────────────────────────────────────

def save_calculation(expression: str, result: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calculations (expression, result) VALUES (%s, %s)",
        (expression, result)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_history(limit: int = 50):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, expression, result, timestamp FROM calculations ORDER BY id DESC LIMIT %s",
        (limit,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert datetime → string for JSON safety
    for r in rows:
        if isinstance(r.get("timestamp"), datetime):
            r["timestamp"] = r["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    return rows

def search_history(query: str):
    pattern = f"%{query}%"
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """SELECT id, expression, result, timestamp 
           FROM calculations 
           WHERE expression LIKE %s OR result LIKE %s 
           ORDER BY id DESC LIMIT 100""",
        (pattern, pattern)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def delete_record(record_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM calculations WHERE id = %s", (record_id,))
    conn.commit()
    cur.close()
    conn.close()

def delete_all():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE calculations")
    conn.commit()
    cur.close()
    conn.close()

def export_csv():
    records = get_history(10000)
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["id", "expression", "result", "timestamp"]
    )
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue()