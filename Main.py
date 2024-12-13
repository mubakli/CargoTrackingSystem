print("hello world");
try:
    import sqlite3
    print("SQLite modülü yüklü ve kullanılabilir.")
except ImportError:
    print("SQLite modülü yüklenmemiş.")