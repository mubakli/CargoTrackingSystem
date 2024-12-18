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

    def add_child(self, child_node, cost):
        self.children.append((child_node, cost))

# Örnek ağaç yapısı oluşturma
def build_tree():
    root = CityNode("Kargo Merkezi", 0, subset=0)

    city_count = 20
    levels = {
        1: [CityNode(f"Şehir {i}", i, subset=1) for i in range(1, 4)],
        2: [CityNode(f"Şehir {i}", i, subset=2) for i in range(4, 7)],
        3: [CityNode(f"Şehir {i}", i, subset=3) for i in range(7, 11)],
        4: [CityNode(f"Şehir {i}", i, subset=4) for i in range(11, city_count + 1)]
    }

    fixed_costs = {
        ("Kargo Merkezi", "Şehir 1"): 5,
        ("Kargo Merkezi", "Şehir 2"): 7,
        ("Kargo Merkezi", "Şehir 3"): 3,
        ("Şehir 1", "Şehir 4"): 4,
        ("Şehir 1", "Şehir 5"): 2,
        ("Şehir 2", "Şehir 6"): 6,
        ("Şehir 4", "Şehir 7"): 5,
        ("Şehir 4", "Şehir 8"): 3,
        ("Şehir 6", "Şehir 9"): 7,
        ("Şehir 6", "Şehir 10"): 4,
        ("Şehir 5", "Şehir 11"): 8,
        ("Şehir 7", "Şehir 12"): 6,
        ("Şehir 8", "Şehir 13"): 9,
        ("Şehir 9", "Şehir 14"): 7,
        ("Şehir 10", "Şehir 15"): 5,
        ("Şehir 10", "Şehir 16"): 6,
        ("Şehir 5", "Şehir 17"): 8,
        ("Şehir 7", "Şehir 18"): 7,
        ("Şehir 8", "Şehir 19"): 5,
        ("Şehir 9", "Şehir 20"): 6
    }

    for child in levels[1]:
        root.add_child(child, cost=fixed_costs[("Kargo Merkezi", child.city_name)])

    levels[1][0].add_child(levels[2][0], cost=fixed_costs[("Şehir 1", "Şehir 4")])
    levels[1][0].add_child(levels[2][1], cost=fixed_costs[("Şehir 1", "Şehir 5")])
    levels[1][1].add_child(levels[2][2], cost=fixed_costs[("Şehir 2", "Şehir 6")])

    levels[2][0].add_child(levels[3][0], cost=fixed_costs[("Şehir 4", "Şehir 7")])
    levels[2][0].add_child(levels[3][1], cost=fixed_costs[("Şehir 4", "Şehir 8")])
    levels[2][2].add_child(levels[3][2], cost=fixed_costs[("Şehir 6", "Şehir 9")])
    levels[2][2].add_child(levels[3][3], cost=fixed_costs[("Şehir 6", "Şehir 10")])

    levels[3][0].add_child(levels[4][0], cost=fixed_costs[("Şehir 7", "Şehir 12")])
    levels[3][1].add_child(levels[4][1], cost=fixed_costs[("Şehir 8", "Şehir 13")])
    levels[3][2].add_child(levels[4][2], cost=fixed_costs[("Şehir 9", "Şehir 14")])
    levels[3][3].add_child(levels[4][3], cost=fixed_costs[("Şehir 10", "Şehir 15")])
    levels[3][3].add_child(levels[4][4], cost=fixed_costs[("Şehir 10", "Şehir 16")])

    levels[2][1].add_child(levels[4][5], cost=fixed_costs[("Şehir 5", "Şehir 17")])
    levels[3][0].add_child(levels[4][6], cost=fixed_costs[("Şehir 7", "Şehir 18")])
    levels[3][1].add_child(levels[4][7], cost=fixed_costs[("Şehir 8", "Şehir 19")])
    levels[3][2].add_child(levels[4][8], cost=fixed_costs[("Şehir 9", "Şehir 20")])

    # Ekstra yollar ekleme (birden fazla gidiş yolu)
    levels[1][0].add_child(levels[3][2], cost=10)  # Şehir 1 -> Şehir 9 (ekstra yol)
    levels[2][0].add_child(levels[4][1], cost=12)  # Şehir 4 -> Şehir 13 (ekstra yol)
    levels[3][3].add_child(levels[2][1], cost=9)   # Şehir 10 -> Şehir 5 (ekstra yol)
    levels[4][0].add_child(levels[4][8], cost=15)  # Şehir 12 -> Şehir 20 (ekstra yol)
    levels[4][1].add_child(levels[4][7], cost=13)  # Şehir 13 -> Şehir 19 (ekstra yol)
    levels[4][2].add_child(levels[4][6], cost=11)  # Şehir 14 -> Şehir 18 (ekstra yol)
    levels[4][3].add_child(levels[4][5], cost=14)  # Şehir 15 -> Şehir 17 (ekstra yol)
    levels[4][4].add_child(levels[4][0], cost=10)  # Şehir 16 -> Şehir 12 (ekstra yol)

    return root

# Ağacı görselleştirme (konsol çıktısı)
def print_tree(node, level=0):
    print("  " * level + f"{node.city_name} (ID: {node.city_id})")
    for child, cost in node.children:
        print("  " * (level + 1) + f"-> {child.city_name} (Maliyet: {cost})")
        print_tree(child, level + 1)

# Ağacın derinliğini hesaplama
def calculate_depth(node):
    if not node.children:
        return 1
    return 1 + max(calculate_depth(child) for child, _ in node.children)

# Bir şehir için alternatif yolları listeleme
def list_routes_to_city(node, target_city_name, current_path=None, current_cost=None, routes=None):
    if current_path is None:
        current_path = []
    if current_cost is None:
        current_cost = []
    if routes is None:
        routes = []

    current_path.append(node.city_name)

    for child, cost in node.children:
        if child.city_name == target_city_name:
            routes.append((current_path + [child.city_name], current_cost + [cost]))
        else:
            list_routes_to_city(child, target_city_name, current_path[:], current_cost[:] + [cost], routes)

    return routes

# En kısa yol hesaplama
def shortest_route_to_city(routes):
    return min(routes, key=lambda x: sum(x[1]), default=(None, []))

# Kullanıcıdan şehir seçimi alıp alternatif yolları ve en kısa yolu gösterme
def select_city_and_show_routes(tree_root):
    target_city = input("Lütfen alternatif yollarını görmek istediğiniz şehri girin: ")
    routes = list_routes_to_city(tree_root, target_city)
    if not routes:
        print(f"{target_city} şehrine ulaşım için bir yol bulunamadı.")
        return

    print(f"\n{target_city} şehrine alternatif yollar:")
    for path, costs in routes:
        detailed_path = " -> ".join(
            [f"{path[i]} (Maliyet: {costs[i - 1]})" if i > 0 else path[i] for i in range(len(path))]
        )
        print(f"Yol: {detailed_path}, Toplam Maliyet: {sum(costs)}")

    shortest_path, shortest_costs = shortest_route_to_city(routes)
    if shortest_path:
        detailed_shortest_path = " -> ".join(
            [f"{shortest_path[i]} (Maliyet: {shortest_costs[i - 1]})" if i > 0 else shortest_path[i] for i in range(len(shortest_path))]
        )
        print(f"\nEn kısa yol: {detailed_shortest_path}, Toplam Maliyet: {sum(shortest_costs)}")

# Ağacı NetworkX grafiği ile görselleştirme
def visualize_tree(node):
    G = nx.DiGraph()

    def add_edges(node):
        for child, cost in node.children:
            G.add_edge(node.city_name, child.city_name, weight=cost)
            G.nodes[child.city_name]["subset"] = child.subset
            add_edges(child)

    G.add_node(node.city_name, subset=node.subset)
    add_edges(node)

    plt.figure(figsize=(12, 8))
    pos = nx.multipartite_layout(G, subset_key="subset")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_colors = ["skyblue" if data["subset"] == 0 else "lightgreen" for _, data in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Şehir Haritası (Ağaç Yapısı)")
    plt.show()

if __name__ == "__main__":
    tree_root = build_tree()
    print("Kargo Rotalama Ağaç Yapısı:")
    print_tree(tree_root)

    depth = calculate_depth(tree_root)
    print(f"\nAğacın Derinliği: {depth}")
    print(f"En Kısa Teslimat Süresi: {depth} birim zaman")

    select_city_and_show_routes(tree_root)

    print("\nŞehir Haritası Görselleştiriliyor...")
    visualize_tree(tree_root)
