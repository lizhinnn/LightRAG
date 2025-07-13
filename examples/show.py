import networkx as nx
from pyvis.network import Network
import random
import webbrowser
import os
from PIL import Image
import io
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def visualize_subgraph(graphml_path, target_node, output_path="subgraph.png"):
    try:
        # 读取 GraphML 文件
        G = nx.read_graphml(graphml_path)
        
        # 检查目标节点是否存在
        if target_node not in G.nodes():
            print(f"错误：节点 '{target_node}' 不存在于图中")
            return
        
        # 获取目标节点的直接邻居
        neighbors = list(G.neighbors(target_node))
        # 创建子图，包含目标节点和其邻居
        subgraph_nodes = [target_node] + neighbors
        subgraph = G.subgraph(subgraph_nodes)
        
        # 创建 Pyvis 网络图
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            cdn_resources='remote',
            directed=True
        )
        
        # 从 NetworkX 子图转换
        net.from_nx(subgraph)
        
        # 为节点添加颜色和其他视觉属性
        for node in net.nodes:
            if node['id'] == target_node:
                # 目标节点使用特殊颜色
                node["color"] = "#FF0000"  # 红色
                node["size"] = 30
            else:
                node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                node["size"] = 25
            node["font"] = {"size": 12}
        
        # 设置布局选项
        net.set_options("""
        {
            "nodes": {
                "font": {
                    "size": 12
                }
            },
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "maxVelocity": 50,
                "solver": "forceAtlas2Based",
                "timestep": 0.35,
                "stabilization": {
                    "enabled": true,
                    "iterations": 1000
                }
            },
            "layout": {
                "improvedLayout": true,
                "hierarchical": {
                    "enabled": false
                }
            }
        }
        """)
        
        # 保存为临时HTML文件
        temp_html = "temp_graph.html"
        net.save_graph(temp_html)
        
        # 使用Selenium将HTML转换为图片
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置窗口大小
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('file://' + os.path.abspath(temp_html))
        
        # 等待图形加载和稳定
        time.sleep(3)  # 增加等待时间确保图形完全加载
        
        # 获取页面截图
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        
        # 保存截图
        with open(output_path, 'wb') as f:
            f.write(screenshot)
        
        # 删除临时HTML文件
        os.remove(temp_html)
        
        print(f"子图已保存到: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    # 使用绝对路径
    graphml_path = r"C:\Users\Dyson\LightragNew\LightRAG\bank\KGbank\ngss0522\graph_chunk_entity_relation.graphml"
    
    # 检查文件是否存在
    if not os.path.exists(graphml_path):
        print(f"错误：GraphML文件未找到: {graphml_path}")
    else:
        # 示例：搜索特定节点
        target_node = "科学课程标准"  # 替换为实际的节点名称
        visualize_subgraph(graphml_path, target_node)
