import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class CityNode:
    def __init__(self, city_name, city_id, subset=0):
        self.city_name = city_name
        self.city_id = city_id
        self.children = []
        self.subset = subset

    def add_child(self, child_node, cost):
        self.children.append((child_node, cost))

def build_tree():
    root = CityNode("Cargo Center", 0, subset=0)

    levels = {
        1: [CityNode(f"City {i}", i, subset=1) for i in range(1, 4)],
        2: [CityNode(f"City {i}", i, subset=2) for i in range(4, 7)],
        3: [CityNode(f"City {i}", i, subset=3) for i in range(7, 11)],
        4: [CityNode(f"City {i}", i, subset=4) for i in range(11, 21)]
    }

    fixed_costs = {
        ("Cargo Center", "City 1"): 5,
        ("Cargo Center", "City 2"): 7,
        ("Cargo Center", "City 3"): 3,
        ("City 1", "City 4"): 4,
        ("City 1", "City 5"): 2,
        ("City 2", "City 6"): 6,
        ("City 4", "City 7"): 5,
        ("City 4", "City 8"): 3,
        ("City 6", "City 9"): 7,
        ("City 6", "City 10"): 4,
        ("City 7", "City 11"): 6,
        ("City 7", "City 12"): 8,
        ("City 8", "City 13"): 9,
        ("City 8", "City 14"): 7,
        ("City 9", "City 15"): 5,
        ("City 9", "City 16"): 6,
        ("City 10", "City 17"): 8,
        ("City 10", "City 18"): 7,
        ("City 5", "City 19"): 5,
        ("City 5", "City 20"): 6
    }

    for child in levels[1]:
        root.add_child(child, cost=fixed_costs[("Cargo Center", child.city_name)])

    levels[1][0].add_child(levels[2][0], cost=fixed_costs[("City 1", "City 4")])
    levels[1][0].add_child(levels[2][1], cost=fixed_costs[("City 1", "City 5")])
    levels[1][1].add_child(levels[2][2], cost=fixed_costs[("City 2", "City 6")])

    levels[2][0].add_child(levels[3][0], cost=fixed_costs[("City 4", "City 7")])
    levels[2][0].add_child(levels[3][1], cost=fixed_costs[("City 4", "City 8")])
    levels[2][2].add_child(levels[3][2], cost=fixed_costs[("City 6", "City 9")])
    levels[2][2].add_child(levels[3][3], cost=fixed_costs[("City 6", "City 10")])

    levels[3][0].add_child(levels[4][0], cost=fixed_costs[("City 7", "City 11")])
    levels[3][0].add_child(levels[4][1], cost=fixed_costs[("City 7", "City 12")])
    levels[3][1].add_child(levels[4][2], cost=fixed_costs[("City 8", "City 13")])
    levels[3][1].add_child(levels[4][3], cost=fixed_costs[("City 8", "City 14")])
    levels[3][2].add_child(levels[4][4], cost=fixed_costs[("City 9", "City 15")])
    levels[3][2].add_child(levels[4][5], cost=fixed_costs[("City 9", "City 16")])
    levels[3][3].add_child(levels[4][6], cost=fixed_costs[("City 10", "City 17")])
    levels[3][3].add_child(levels[4][7], cost=fixed_costs[("City 10", "City 18")])

    # Add more alternative routes
    for level in levels.values():
        for city in level:
            if len(city.children) < 2:
                for other_level in levels.values():
                    for potential_child in other_level:
                        if potential_child != city and all(potential_child != child[0] for child in city.children):
                            if potential_child.city_id > city.city_id:  # Ensure no back connections
                                city.add_child(potential_child, cost=10)  # Default extra cost
                                if len(city.children) >= 2:
                                    break
                    if len(city.children) >= 2:
                        break

    return root

def list_routes_to_city(node, target_city_name, current_path=None, current_cost=None, routes=None, visited=None):
    if current_path is None:
        current_path = []
    if current_cost is None:
        current_cost = []
    if routes is None:
        routes = []
    if visited is None:
        visited = set()

    if node.city_id in visited:
        return routes

    visited.add(node.city_id)
    current_path.append(node.city_name)

    for child, cost in node.children:
        if child.city_name == target_city_name:
            routes.append((current_path + [child.city_name], current_cost + [cost]))
        else:
            list_routes_to_city(
                child,
                target_city_name,
                current_path[:],
                current_cost[:] + [cost],
                routes,
                visited.copy()
            )

    return routes

def shortest_route_to_city(routes):
    return min(routes, key=lambda x: sum(x[1]), default=(None, []))

def visualize_tree(node, target_city_name):
    G = nx.DiGraph()

    def add_edges(node, visited=None):
        if visited is None:
            visited = set()

        if node.city_id in visited:
            return

        visited.add(node.city_id)

        for child, cost in node.children:
            G.add_edge(node.city_name, child.city_name, weight=cost)
            G.nodes[child.city_name]["subset"] = child.subset
            add_edges(child, visited)

    G.add_node(node.city_name, subset=node.subset)
    add_edges(node)

    pos = nx.multipartite_layout(G, subset_key="subset")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_colors = ["skyblue" if data["subset"] == 0 else "lightgreen" for _, data in G.nodes(data=True)]
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(f"Route to {target_city_name}")
    plt.show()

def fetch_all_shipments():
    conn = sqlite3.connect('shipping.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT shipping_id, shipping_date, delivery_status, delivery_time, customer_id, target_city_id
        FROM shipping_history
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def show_routes(event):
    selected_item = shipments_tree.selection()
    if not selected_item:
        return
    target_city_id = shipments_tree.item(selected_item, "values")[5]
    target_city_name = f"City {target_city_id}"

    routes = list_routes_to_city(tree_root, target_city_name)
    if not routes:
        messagebox.showinfo("No Routes", f"No routes found to {target_city_name}.")
        return

    shortest_path, shortest_costs = shortest_route_to_city(routes)
    detailed_shortest_path = " -> ".join(
        [f"{shortest_path[i]} (Cost: {shortest_costs[i - 1]})" if i > 0 else shortest_path[i] for i in range(len(shortest_path))]
    )
    messagebox.showinfo("Shortest Route", f"Shortest route to {target_city_name}:\n{detailed_shortest_path}\nTotal Cost: {sum(shortest_costs)}")

    visualize_tree(tree_root, target_city_name)


def open_visualization_window():
    window = tk.Toplevel()
    window.title("Cargo Routes Visualization")
    window.geometry("800x600")

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    G = nx.DiGraph()

    def add_edges(node, visited=None):
        if visited is None:
            visited = set()

        if node.city_id in visited:
            return

        visited.add(node.city_id)

        for child, cost in node.children:
            G.add_edge(node.city_name, child.city_name, weight=cost)
            G.nodes[child.city_name]["subset"] = child.subset
            add_edges(child, visited)

    G.add_node(tree_root.city_name, subset=tree_root.subset)
    add_edges(tree_root)

    pos = nx.multipartite_layout(G, subset_key="subset")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_colors = ["skyblue" if data["subset"] == 0 else "lightgreen" for _, data in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight="bold", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    ax.set_title("Cargo Routes Visualization")

    canvas.draw()

    # Add magnification tools
    def zoom(event):
        base_scale = 1.1
        scale = base_scale if event.delta > 0 else 1 / base_scale
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        canvas.draw()

    def pan(event):
        if event.button == 1 and pan.start:
            dx = event.xdata - pan.start[0]
            dy = event.ydata - pan.start[1]
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            ax.set_xlim([cur_xlim[0] - dx, cur_xlim[1] - dx])
            ax.set_ylim([cur_ylim[0] - dy, cur_ylim[1] - dy])
            canvas.draw()

    def on_press(event):
        pan.start = (event.xdata, event.ydata)

    def on_release(event):
        pan.start = None

    def zoom_in():
        zoom_event = type('test', (object,), {'delta': 1, 'xdata': (ax.get_xlim()[1] + ax.get_xlim()[0]) / 2, 'ydata': (ax.get_ylim()[1] + ax.get_ylim()[0]) / 2})()
        zoom(zoom_event)

    def zoom_out():
        zoom_event = type('test', (object,), {'delta': -1, 'xdata': (ax.get_xlim()[1] + ax.get_xlim()[0]) / 2, 'ydata': (ax.get_ylim()[1] + ax.get_ylim()[0]) / 2})()
        zoom(zoom_event)

    fig.canvas.mpl_connect('scroll_event', zoom)
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('motion_notify_event', pan)

    pan.start = None

    zoom_in_button = ttk.Button(window, text="Zoom In", command=zoom_in)
    zoom_in_button.pack(side=tk.LEFT, padx=10, pady=10)

    zoom_out_button = ttk.Button(window, text="Zoom Out", command=zoom_out)
    zoom_out_button.pack(side=tk.LEFT, padx=10, pady=10)

    window.mainloop()
def main():
    global shipments_tree, tree_root

    tree_root = build_tree()

    root = tk.Tk()
    root.title("Cargo Routes")

    frame_left = ttk.Frame(root)
    frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_right = ttk.Frame(root)
    frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    shipments_tree = ttk.Treeview(frame_left, columns=("ID", "Date", "Status", "Time", "Customer ID", "Target City ID"), show="headings")
    shipments_tree.heading("ID", text="ID")
    shipments_tree.heading("Date", text="Date")
    shipments_tree.heading("Status", text="Status")
    shipments_tree.heading("Time", text="Time")
    shipments_tree.heading("Customer ID", text="Customer ID")
    shipments_tree.heading("Target City ID", text="Target City ID")
    shipments_tree.pack(expand=True, fill="both")

    shipments = fetch_all_shipments()
    for shipment in shipments:
        shipments_tree.insert("", "end", values=shipment)

    shipments_tree.bind("<Double-1>", show_routes)

    ttk.Button(frame_right, text="Visualize Routes", command=open_visualization_window).pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()