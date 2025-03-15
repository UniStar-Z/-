import sqlite3
from pathlib import Path
from config.settings import DATABASE_PATH

# 首次运行时自动创建数据库和表结构
if not Path(DATABASE_PATH).exists():
    conn = sqlite3.connect(DATABASE_PATH)
    with open('data_management/init_db.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()