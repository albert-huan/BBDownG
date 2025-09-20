#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量下载功能测试脚本
用于验证URL解析和文件读取功能
"""

import os
import re
import configparser


def is_valid_url(url):
    """检查是否为有效的B站视频URL"""
    if not url:
        return False
    
    # B站视频URL模式
    patterns = [
        r'https?://www\.bilibili\.com/video/[Bb][Vv]\w+',
        r'https?://b23\.tv/\w+',
        r'https?://www\.bilibili\.com/bangumi/play/[Ee][Pp]\d+',
        r'https?://www\.bilibili\.com/bangumi/play/ss\d+',
        r'[Bb][Vv]\w+',
        r'[Ee][Pp]\d+',
        r'ss\d+'
    ]
    
    return any(re.match(pattern, url.strip()) for pattern in patterns)


def load_urls_from_file(file_path):
    """从文件加载URL列表"""
    urls = []
    
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在")
        return urls
    
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.ini':
            # 解析INI文件
            config = configparser.ConfigParser()
            config.read(file_path, encoding='utf-8')
            
            for section in config.sections():
                for key, value in config.items(section):
                    if is_valid_url(value):
                        urls.append(value.strip())
                    elif is_valid_url(key):
                        urls.append(key.strip())
        
        else:
            # 解析TXT文件
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and is_valid_url(line):
                    urls.append(line)
        
        # 去重
        urls = list(dict.fromkeys(urls))
        
    except Exception as e:
        print(f"读取文件失败：{str(e)}")
    
    return urls


def test_url_validation():
    """测试URL验证功能"""
    print("=== 测试URL验证功能 ===")
    
    test_urls = [
        "https://www.bilibili.com/video/BV1xx411c7mu",
        "https://b23.tv/BV1xx411c7mu", 
        "https://www.bilibili.com/bangumi/play/ep123456",
        "https://www.bilibili.com/bangumi/play/ss12345",
        "BV1xx411c7mu",
        "ep123456",
        "ss12345",
        "invalid_url",
        "",
        "https://www.youtube.com/watch?v=123"
    ]
    
    for url in test_urls:
        result = is_valid_url(url)
        print(f"URL: {url:<50} 有效: {result}")


def test_file_parsing():
    """测试文件解析功能"""
    print("\n=== 测试文件解析功能 ===")
    
    # 测试TXT文件
    if os.path.exists("example_urls.txt"):
        print("\n--- 解析 example_urls.txt ---")
        urls = load_urls_from_file("example_urls.txt")
        print(f"找到 {len(urls)} 个有效URL:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
    
    # 测试INI文件
    if os.path.exists("example_urls.ini"):
        print("\n--- 解析 example_urls.ini ---")
        urls = load_urls_from_file("example_urls.ini")
        print(f"找到 {len(urls)} 个有效URL:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")


def main():
    """主测试函数"""
    print("BBDownG 批量下载功能测试")
    print("=" * 50)
    
    test_url_validation()
    test_file_parsing()
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()