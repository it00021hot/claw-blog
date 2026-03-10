#!/usr/bin/env python3
import os
import re
from datetime import datetime

# 配置
OFFICIAL_DOCS_DIR = "/Users/zhihu/projects/openclaw/openclaw/docs/zh-CN"
EN_OFFICIAL_DOCS_DIR = "/Users/zhihu/projects/openclaw/openclaw/docs"
OUTPUT_DIR = "/Users/zhihu/projects/claw-blog/content/openclaw/docs"
DEFAULT_CATEGORY = "OpenClaw官方文档"
DEFAULT_TAGS = ["OpenClaw", "官方文档", "技术文档"]

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_title(content):
    """从markdown内容中提取第一个标题作为文章标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名文档"

def process_markdown(file_path, is_zh=True):
    """处理单个markdown文件，添加hugo front matter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 去掉原文件开头的front matter（如果有的话）
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # 提取标题
    title = extract_title(content)
    if not title:
        # 从文件名生成标题
        filename = os.path.basename(file_path)
        title = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
    
    # 转义title里的双引号
    title = title.replace('"', '\\"')
    
    # 去掉开头的第一个标题（已经放在front matter里了）
    content = re.sub(r'^#\s+.+$\n', '', content, count=1, flags=re.MULTILINE)
    
    # 处理相对链接，指向官方文档站点
    content = re.sub(r'\(([^)]+\.md)\)', r'(https://docs.openclaw.ai/\1)', content)
    
    # 生成front matter
    date_str = datetime.now().strftime("%Y-%m-%d")
    front_matter = f"""---
title: "{title}"
date: {date_str}
categories: ["{DEFAULT_CATEGORY}"]
tags: ["OpenClaw", "官方文档", "技术文档"]
draft: false
---
"""
    
    # 组合内容
    final_content = front_matter + content
    
    # 生成输出路径
    rel_path = os.path.relpath(file_path, OFFICIAL_DOCS_DIR if is_zh else EN_OFFICIAL_DOCS_DIR)
    output_path = os.path.join(OUTPUT_DIR, rel_path)
    
    # 确保输出子目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ 处理完成: {rel_path}")

def process_directory(dir_path, is_zh=True):
    """递归处理目录下的所有markdown文件"""
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md') and not file.startswith('_'):
                file_path = os.path.join(root, file)
                try:
                    process_markdown(file_path, is_zh)
                except Exception as e:
                    print(f"❌ 处理失败 {file_path}: {str(e)}")

if __name__ == "__main__":
    print("开始导入中文官方文档...")
    if os.path.exists(OFFICIAL_DOCS_DIR):
        process_directory(OFFICIAL_DOCS_DIR, is_zh=True)
    else:
        print("⚠️  中文文档不存在，导入英文文档...")
        process_directory(EN_OFFICIAL_DOCS_DIR, is_zh=False)
    
    print("\n🎉 所有文档导入完成！")
