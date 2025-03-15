import csv
from pathlib import Path
import sqlite3
import json
from config.settings import DATABASE_PATH  # 数据库路径注释

def init_db(path):
    """初始化数据库连接"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detection (
            id INTEGER PRIMARY KEY,
            image_path TEXT NOT NULL,
            defect JSON NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def save_record(path, image_path, result):
    """保存检测记录（数据库操作）"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO detection (image_path, defect) 
        VALUES (?, ?)
    """, (image_path, json.dumps(result)))
    conn.commit()
    
def get_detection_records(path):
    """获取所有检测记录（新增函数）"""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM detection")
    records = cursor.fetchall()
    # 转换为JSON格式列表
    return [json.loads(row[2]) for row in records]

def export_to_csv(db_path: str, output_path: str):
    """将检测记录导出为CSV文件
    
    Args:
        db_path: SQLite数据库路径
        output_path: CSV文件输出路径
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询所有记录
        cursor.execute("SELECT * FROM detection")
        records = cursor.fetchall()
        
        # 定义CSV列名（需与表结构对应）
        fieldnames = ["id", "image_path", "defects", "timestamp"]
        
        # 写入CSV文件
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for row in records:
                # 将JSON字段转为字符串
                formatted_row = list(row)
                formatted_row[2] = str(formatted_row[2])  # defects字段
                writer.writerow(formatted_row)
                
    except sqlite3.Error as e:
        raise RuntimeError(f"数据库操作失败: {str(e)}")
    except IOError as e:
        raise RuntimeError(f"文件写入失败: {str(e)}")
    finally:
        conn.close()