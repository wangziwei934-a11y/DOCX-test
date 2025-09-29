#!/usr/bin/env python3
"""
本地测试 DOC-Dify-Plugin 的脚本
用于在没有 Dify 环境的情况下测试插件功能
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

# 使用模拟的 dify_plugin 模块
sys.modules['dify_plugin'] = __import__('mock_dify_plugin')
sys.modules['dify_plugin.entities.tool'] = __import__('mock_dify_plugin')

# 现在导入我们的工具
from tools.doc import DocTool

def test_doc_tool():
    """测试 DocTool 的基本功能"""
    print("🚀 开始测试 DocTool...")
    
    # 创建工具实例
    tool = DocTool()
    
    # 准备测试数据
    test_markdown = """
# 第一章 概述
这是第一章的内容介绍。

1. 背景介绍
2. 目标设定
3. 范围定义

## 第二章 方法
这是第二章的具体方法。

1. 数据收集方法
2. 数据分析技术
3. 结果验证流程

### 2.1 数据处理
详细的数据处理步骤：

1. 数据清洗
2. 数据转换
3. 数据验证

| 方法 | 描述 | 优点 |
|------|------|------|
| 方法A | 快速处理 | 效率高 |
| 方法B | 精确处理 | 准确性高 |

图表展示：
ECharts图表会被过滤掉

## 第三章 结果
分析结果如下：

1. 主要发现
2. 重要结论
3. 建议事项
"""
    
    tool_parameters = {
        "markdown_content": test_markdown,
        "title": "测试文档"
    }
    
    print("📝 测试输入:")
    print(f"标题: {tool_parameters['title']}")
    print(f"内容长度: {len(test_markdown)} 字符")
    print()
    
    # 调用工具
    print("⚙️ 执行转换...")
    try:
        messages = list(tool._invoke(tool_parameters))
        
        print("✅ 转换完成!")
        print(f"📊 生成了 {len(messages)} 个消息")
        
        for i, message in enumerate(messages, 1):
            print(f"消息 {i}: {message.type}")
            if message.type == "text":
                print(f"  文本: {message.message}")
            elif message.type == "blob":
                print(f"  文件: {message.meta.get('filename', '未知')}")
                print(f"  大小: {len(message.blob)} 字节")
                print(f"  类型: {message.meta.get('mime_type', '未知')}")
                
                # 保存文件到本地
                filename = message.meta.get('filename', 'output.docx')
                with open(filename, 'wb') as f:
                    f.write(message.blob)
                print(f"  ✅ 已保存到: {filename}")
            print()
            
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()

def test_numbering():
    """测试编号转换功能"""
    print("🔢 测试编号转换功能...")
    
    tool = DocTool()
    
    # 测试编号转换
    test_texts = [
        "1. 第一项内容",
        "2、第二项内容", 
        "3）第三项内容",
        "（4）第四项内容",
        "5. 第五项内容",
    ]
    
    for text in test_texts:
        converted = tool._convert_number_labels(text)
        print(f"原文: {text}")
        print(f"转换: {converted}")
        print()

def test_chart_filtering():
    """测试图表过滤功能"""
    print("🎯 测试图表过滤功能...")
    
    tool = DocTool()
    
    test_texts = [
        "ECharts图表",
        "图表展示：数据分析", 
        "图表说明",
        "这是正常的文字内容",
        "数据可视化展示",
        "柱状图显示结果"
    ]
    
    for text in test_texts:
        is_filtered = tool._is_chart_related_text(text)
        status = "🚫 过滤" if is_filtered else "✅ 保留"
        print(f"{status}: {text}")

if __name__ == "__main__":
    print("=" * 50)
    print("DOC-Dify-Plugin 本地测试")
    print("=" * 50)
    print()
    
    # 运行所有测试
    test_chart_filtering()
    print()
    test_numbering()
    print()
    test_doc_tool()
    
    print("=" * 50)
    print("测试完成!")
    print("=" * 50)














