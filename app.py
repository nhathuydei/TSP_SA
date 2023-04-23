import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QGridLayout, QWidget, QFileDialog, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tìm đường đi tốt nhất")
        self.central_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.start_node_combo_box = QComboBox(self.central_widget)
        self.start_node_label = QLabel("Điểm xuất phát", self.central_widget)
        self.start_button = QPushButton("Bắt đầu", self.central_widget)
        self.start_button.clicked.connect(self.start_algorithm)
        self.grid_layout.addWidget(self.start_node_label, 0, 0)
        self.grid_layout.addWidget(self.start_node_combo_box, 0, 1)
        self.grid_layout.addWidget(self.start_button, 2, 0, 1, 2)
        self.nodes = ["A", "B", "C", "D", "E", "F"]
        self.edges = [("A", "B", 6), ("A", "D", 4), ("A", "E", 3), ("A", "F", 5),
                      ("B", "C", 5), ("B", "D", 4), ("B", "F", 4),
                      ("C", "D", 3), ("C", "E", 5),
                      ("D", "E", 3),
                      ("E", "F", 3),
                      ("F", "B", 4)]
        self.graph = nx.Graph()
        self.graph.add_weighted_edges_from(self.edges)
        self.path = []
        self.path_cost = 0
        self.current_node = None
        self.start_node_combo_box.addItems(self.nodes)
        self.total_cost_label = QLabel(self.central_widget)
        self.grid_layout.addWidget(self.total_cost_label, 3, 0, 1, 2)

    def simulated_annealing(self, graph, start):
        temperature = 1000
        cooling_rate = 0.003
        current_node = start
        path = [current_node]
        path_cost = 0

        # Check if start node has any neighbors
        if not list(graph.neighbors(current_node)):
            return [], math.inf

        while temperature > 1:
            neighbors = list(graph.neighbors(current_node))
            next_node = random.choice(neighbors)
            if next_node not in path:
                if next_node == start:
                    path.append(next_node)
                    path_cost += graph[current_node][next_node]["weight"]
                    return path, path_cost
                new_path_cost = path_cost + graph[current_node][next_node]["weight"]
                if new_path_cost < path_cost or random.uniform(0, 1) < math.exp((path_cost - new_path_cost) / temperature):
                    path.append(next_node)
                    path_cost = new_path_cost
                    current_node = next_node
            temperature *= 1 - cooling_rate
        path.append(start)
        path_cost = path_cost + graph[current_node][start]["weight"]
        return path, path_cost

    def start_algorithm(self):
        start_node = self.start_node_combo_box.currentText()
        self.path, self.path_cost = self.simulated_annealing(self.graph, start_node)
        self.current_node = start_node
        self.draw_graph()
        self.total_cost_label.setText("Tổng chi phí: " + str(self.path_cost))

    def draw_graph(self):
      pos = nx.spring_layout(self.graph)
      edge_labels = nx.get_edge_attributes(self.graph, "weight")
      nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=500)
      nx.draw_networkx_labels(self.graph, pos, font_size=14, font_family="sans-serif")
      nx.draw_networkx_edges(self.graph, pos)
      nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=12, font_color="red")
      for i in range(len(self.path) - 1):
          nx.draw_networkx_edges(self.graph, pos, edgelist=[(self.path[i], self.path[i + 1])],
                                edge_color="blue", width=2.0)
      plt.axis("off")
      plt.show()

    def update_graph(self):
      pos = nx.spring_layout(self.graph)
      edge_labels = nx.get_edge_attributes(self.graph, "weight")
      nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=500)
      nx.draw_networkx_labels(self.graph, pos, font_size=14, font_family="sans-serif")
      nx.draw_networkx_edges(self.graph, pos)
      nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=12, font_color="red")
      for i in range(len(self.path) - 1):
          nx.draw_networkx_edges(self.graph, pos, edgelist=[(self.path[i], self.path[i + 1])],
                                edge_color="blue", width=2.0)
      nx.draw_networkx_edges(self.graph, pos, edgelist=[(self.current_node, self.path[0])], edge_color="green",
                            width=2.0)
      plt.axis("off")
      plt.show()

if __name__ == "__main__":
  app = QApplication([])
  main_window = MainWindow()
  main_window.show()
  app.exec()