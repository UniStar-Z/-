-- 创建表结构
CREATE TABLE IF NOT EXISTS detection (
    id INTEGER PRIMARY KEY,
    image_path TEXT NOT NULL,
    defect JSON NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建缺陷类型字典表
CREATE TABLE IF NOT EXISTS defect_types (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

INSERT INTO defect_types (name) VALUES
('夹杂物'),  -- 对应数据集中的"inclusion"
('划痕'),     -- 对应数据集中的"scratch"
('补丁'),     -- 对应数据集中的"patch"
('其他');     -- 其他未分类缺陷
