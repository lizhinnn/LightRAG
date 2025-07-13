# import pipmaster as pm

# if not pm.is_installed("pyvis"):
#     pm.install("pyvis")
# if not pm.is_installed("networkx"):
#     pm.install("networkx")

# import networkx as nx
# from pyvis.network import Network
# import random

# # Load the GraphML file
# G = nx.read_graphml(r"bank\KGbank\Nofigure0429\graph_chunk_entity_relation.graphml")

# # Create a Pyvis network
# net = Network(height="100vh", notebook=True)

# # Convert NetworkX graph to Pyvis network
# net.from_nx(G)


# # Add colors and title to nodes
# for node in net.nodes:
#     node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
#     if "description" in node:
#         node["title"] = node["description"]

# # Add title to edges
# for edge in net.edges:
#     if "description" in edge:
#         edge["title"] = edge["description"]

# # Save and display the network
# net.show("knowledge_graph.html")




import networkx as nx
from pyvis.network import Network
import random
import webbrowser
import os

def visualize_graph(graphml_path, output_path=r"C:\Users\Dyson\LightragNew\LightRAG\bank\KGbank\ngss0522\knowledge_graph.html"):
    try:
        # 读取 GraphML 文件
        G = nx.read_graphml(graphml_path)
        
        # 创建 Pyvis 网络图
        net = Network(
            height="750px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
            cdn_resources='remote',
            directed=True  # 添加这个参数以支持有向图
        )
        
        # 从 NetworkX 图转换
        net.from_nx(G)
        
        # 为节点添加随机颜色和其他视觉属性
        for node in net.nodes:
            node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            node["size"] = 25  # 调整节点大小
            node["font"] = {"size": 12}  # 调整字体大小
        
        # 保存网络图
        net.save_graph(output_path)
        print(f"Graph saved to: {os.path.abspath(output_path)}")
        
        # 自动在默认浏览器中打开生成的文件
        webbrowser.open('file://' + os.path.abspath(output_path))
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # 使用绝对路径
    graphml_path = r"C:\Users\Dyson\LightragNew\LightRAG\bank\KGbank\ngss0522\graph_chunk_entity_relation.graphml"
    
    # 检查文件是否存在
    if not os.path.exists(graphml_path):
        print(f"Error: GraphML file not found at {graphml_path}")
    else:
        visualize_graph(graphml_path)
