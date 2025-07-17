import sqlite3
from pathlib import Path

db_path = Path("inbound_api.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla de cargas
cursor.execute("""
CREATE TABLE IF NOT EXISTS loads (
    load_id TEXT PRIMARY KEY,
    origin TEXT,
    destination TEXT,
    pickup_datetime TEXT,
    delivery_datetime TEXT,
    equipment_type TEXT,
    loadboard_rate INTEGER,
    notes TEXT
);
""")

# Crear tabla de logs de llamadas
cursor.execute("""
CREATE TABLE IF NOT EXISTS call_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mc_number TEXT,
    load_id TEXT,
    final_rate INTEGER,
    outcome TEXT,
    sentiment TEXT,
    negotiation_rounds INTEGER,
    timestamp TEXT
);
""")

# Insertar datos de prueba
sample_loads = [
    ("L001", "Atlanta, GA", "Miami, FL", "2025-07-18T10:00:00", "2025-07-19T18:00:00", "Dry Van", 1200, "Urgent delivery"),
    ("L002", "Dallas, TX", "Phoenix, AZ", "2025-07-19T08:00:00", "2025-07-20T15:00:00", "Reefer", 1450, "")
]

cursor.executemany("""
INSERT OR REPLACE INTO loads (load_id, origin, destination, pickup_datetime, delivery_datetime, equipment_type, loadboard_rate, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", sample_loads)

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
