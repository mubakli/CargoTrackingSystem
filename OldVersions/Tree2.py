import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  # PyCharm ile uyumlu bir backend

class CityNode:
    def __init__(self, city_name, city_id, subset=0):
        self.city_name = city_name
        self.city_id = city_id
        self.children = []
        self.subset = subset

    def add_child(self, child_node):
        self.children.append(child_node)

# Örnek ağaç yapısı oluşturma
def build_tree():
    root = CityNode("Kargo Merkezi", 0, subset=0)

    # Birinci seviye şehirler
    city1 = CityNode("Şehir 1", 1, subset=1)
    city2 = CityNode("Şehir 2", 2, subset=1)
    city3 = CityNode("Şehir 3", 3, subset=1)

    root.add_child(city1)
    root.add_child(city2)
    root.add_child(city3)

    # İkinci seviye şehirler
    city4 = CityNode("Şehir 4", 4, subset=2)
    city5 = CityNode("Şehir 5", 5, subset=2)
    city6 = CityNode("Şehir 6", 6, subset=2)

    city1.add_child(city4)
    city1.add_child(city5)
    city2.add_child(city6)

    # Üçüncü seviye şehirler
    city7 = CityNode("Şehir 7", 7, subset=3)
    city8 = CityNode("Şehir 8", 8, subset=3)
    city9 = CityNode("Şehir 9", 9, subset=3)
    city10 = CityNode("Şehir 10", 10, subset=3)

    city4.add_child(city7)
    city4.add_child(city8)
    city6.add_child(city9)
    city6.add_child(city10)

    # Daha fazla şehir ekleme
    city11 = CityNode("Şehir 11", 11, subset=4)
    city12 = CityNode("Şehir 12", 12, subset=4)
    city13 = CityNode("Şehir 13", 13, subset=4)
    city14 = CityNode("Şehir 14", 14, subset=4)
    city15 = CityNode("Şehir 15", 15, subset=4)
    city16 = CityNode("Şehir 16", 16, subset=4)
    city17 = CityNode("Şehir 17", 17, subset=4)
    city18 = CityNode("Şehir 18", 18, subset=4)
    city19 = CityNode("Şehir 19", 19, subset=4)
    city20 = CityNode("Şehir 20", 20, subset=4)

    city2.add_child(city11)
    city3.add_child(city12)
    city3.add_child(city13)
    city5.add_child(city14)
    city5.add_child(city15)
    city7.add_child(city16)
    city8.add_child(city17)
    city9.add_child(city18)
    city10.add_child(city19)
    city10.add_child(city20)

    return root

# Ağacı görselleştirme (konsol çıktısı)
def print_tree(node, level=0):
    print("  " * level + f"{node.city_name} (ID: {node.city_id})")
    for child in node.children:
        print_tree(child, level + 1)

# Ağacın derinliğini hesaplama
def calculate_depth(node):
    if not node.children:
        return 1
    return 1 + max(calculate_depth(child) for child in node.children)

# Ağacı NetworkX grafiği ile görselleştirme
def visualize_tree(node):
    G = nx.DiGraph()

    def add_edges(node):
        for child in node.children:
            G.add_edge(node.city_name, child.city_name)
            G.nodes[child.city_name]["subset"] = child.subset
            add_edges(child)

    G.add_node(node.city_name, subset=node.subset)
    add_edges(node)

    plt.figure(figsize=(12, 8))
    pos = nx.multipartite_layout(G, subset_key="subset")
    edge_colors = ["gray" for _ in G.edges]
    node_colors = ["skyblue" if data["subset"] == 0 else "lightgreen" for _, data in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold", edge_color=edge_colors)
    plt.title("Şehir Haritası (Ağaç Yapısı)")
    plt.show()

if __name__ == "__main__":
    tree_root = build_tree()
    print("Kargo Rotalama Ağaç Yapısı:")
    print_tree(tree_root)

    depth = calculate_depth(tree_root)
    print(f"\nAğacın Derinliği: {depth}")
    print(f"En Kısa Teslimat Süresi: {depth} birim zaman")

    print("\nŞehir Haritası Görselleştiriliyor...")
    visualize_tree(tree_root)
