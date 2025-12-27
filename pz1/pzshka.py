import sqlite3
from datetime import datetime

DB_NAME = "security_events.db"


# ex1
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #Підтримка FOREIGN KEY
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE,
            severity TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        )
    """)

    conn.commit()
    conn.close()


#ex2
def add_event_source(name, location, source_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO EventSources (name, location, type) VALUES (?, ?, ?)",
        (name, location, source_type)
    )

    conn.commit()
    conn.close()


#ex2
def add_event_type(type_name, severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO EventTypes (type_name, severity) VALUES (?, ?)",
        (type_name, severity)
    )

    conn.commit()
    conn.close()


#ex3
def add_security_event(source_id, event_type_id, message, ip=None, username=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO SecurityEvents
        (timestamp, source_id, event_type_id, message, ip_address, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source_id,
        event_type_id,
        message,
        ip,
        username
    ))

    conn.commit()
    conn.close()


#ex4
def login_failed_last_24h():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM SecurityEvents
        WHERE event_type_id = (
            SELECT id FROM EventTypes WHERE type_name = 'Login Failed'
        )
        AND timestamp >= datetime('now', '-1 day')
    """)

    result = cursor.fetchall()
    conn.close()
    return result


#ex4
def brute_force_ips():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip_address, COUNT(*)
        FROM SecurityEvents
        WHERE event_type_id = (
            SELECT id FROM EventTypes WHERE type_name = 'Login Failed'
        )
        AND timestamp >= datetime('now', '-1 hour')
        GROUP BY ip_address
        HAVING COUNT(*) > 5
    """)

    result = cursor.fetchall()
    conn.close()
    return result


#ex4
def critical_events_last_week():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT es.name, COUNT(*)
        FROM SecurityEvents se
        JOIN EventSources es ON se.source_id = es.id
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.severity = 'Critical'
        AND se.timestamp >= datetime('now', '-7 day')
        GROUP BY es.name
    """)

    result = cursor.fetchall()
    conn.close()
    return result


#ex4
def search_by_keyword(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM SecurityEvents
        WHERE message LIKE ?
    """, (f"%{keyword}%",))

    result = cursor.fetchall()
    conn.close()
    return result


#ex5
if __name__ == "__main__":
    create_database()

    # Типи
    add_event_type("Login Success", "Informational")
    add_event_type("Login Failed", "Warning")
    add_event_type("Port Scan Detected", "Warning")
    add_event_type("Malware Alert", "Critical")

    # Джерело
    add_event_source("Firewall_A", "192.168.1.1", "Firewall")
    add_event_source("Web_Server_Logs", "10.0.0.5", "Web Server")

    # Тест
    for _ in range(7):
        add_security_event(
            source_id=1,
            event_type_id=2,
            message="Failed login attempt",
            ip="83.149.9.216",
            username="admin"
        )

    add_security_event(
        source_id=2,
        event_type_id=4,
        message="Trojan detected",
        ip="66.249.73.135"
    )

    #Демонстрація
    print("Login Failed (24h):", login_failed_last_24h())
    print("Brute-force IPs:", brute_force_ips())
    print("Critical events:", critical_events_last_week())
    print("Keyword 'Trojan':", search_by_keyword("Trojan"))
