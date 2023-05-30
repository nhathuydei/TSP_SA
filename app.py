import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton, QGridLayout, QWidget, QFileDialog, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        # gọi hàm tạo của QMainWindow
        super().__init__()
        # đặt tiêu đề cho cửa sổ
        self.setWindowTitle("Tìm đường đi tối ưu")
        # tạo widget trung tâm cho cửa sổ chính
        self.central_widget = QWidget(self)
        # tạo bố cục dạng lưới cho widget trung tâm
        self.grid_layout = QGridLayout(self.central_widget)
        # đặt widget trung tâm cho cửa sổ chính
        self.setCentralWidget(self.central_widget)
        # tạo box chọn nút bắt đầu
        self.start_node_combo_box = QComboBox(self.central_widget)
        # tạo label (nhãn tên) cho box
        self.start_node_label = QLabel("Điểm xuất phát", self.central_widget)
        # tạo một nút bắt đầu giải thuật
        self.start_button = QPushButton("Bắt đầu", self.central_widget)
        # kết nối nút bắt đầu với hàm bắt đầu thuật toán
        self.start_button.clicked.connect(self.start_algorithm)
        # thêm label, box và nút bắt đầu vào vị trí chỉ định trong bố cục dạng lưới
        self.grid_layout.addWidget(self.start_node_label, 0, 0)
        self.grid_layout.addWidget(self.start_node_combo_box, 0, 1)
        self.grid_layout.addWidget(self.start_button, 2, 0, 1, 2)
        # xác định danh sách các nodes và danh sách các đường đi (cạnh) cho graph
        self.nodes = ["A", "B", "C", "D", "E", "F"]
        self.edges = [("A", "B", 6), ("A", "D", 4), ("A", "E", 3), ("A", "F", 5), ("A", "C", 7),
                      ("B", "C", 5), ("B", "D", 4), ("B", "F", 4),("B", "E", 3),
                      ("C", "D", 3), ("C", "E", 5), ("C", "F", 4),
                      ("D", "E", 3), ("D", "F", 4),
                      ("E", "F", 3)]
        # tạo một object đồ thị vô hướng mới
        self.graph = nx.Graph()
        # thêm cạnh và chi phí vào đồ thị
        self.graph.add_weighted_edges_from(self.edges)
        # khởi tạo một list trống dùng để lưu trữ chuỗi các node trong đường dẫn, từ node bắt đầu đến node kết thúc
        self.path = []
        # khởi tạo biến tổng chi phí của path bằng 0, tính từ node bắt đầu đến node kết thúc
        self.path_cost = 0
        # khởi tạo biến node hiện tại là None, biến này dùng để keep track với node hiện tại 
        self.current_node = None
        # thêm node bắt đầu và node kết thúc tương ứng từ list node trong graph
        self.start_node_combo_box.addItems(self.nodes)
        # tạo label và thêm nó vào vị trí chỉ định trong bố cục lưới, label dùng để hiện tổng chi phí từ node bắt đầu đến node kết thúc
        self.total_cost_label = QLabel(self.central_widget)
        self.grid_layout.addWidget(self.total_cost_label, 3, 0, 1, 2)

    def simulated_annealing(self, graph, start):
        temperature = 1000
        cooling_rate = 0.003
        current_node = start
        path = [current_node]
        path_cost = 0

        # Kiểm tra xem node bắt đầu có node lân cận nào không
        if not list(graph.neighbors(current_node)):
            return [], math.inf

        while temperature > 1:
            # khởi tạo biến neighbors là một node lân cận ngẫu nhiên của node hiện tại làm node tiếp theo để xét  
            neighbors = list(graph.neighbors(current_node))
            next_node = random.choice(neighbors) 
            # kiểm tra nếu node tiếp theo này đã visited (mỗi node chỉ sử dụng một lần), thuật toán bỏ qua node đó. 
            # Nếu không thì tiếp tục
            if next_node not in path:
                # kiểm tra nếu node tiếp theo là node kết thúc, thuật toán nối nó vào path và 
                # thêm chi phí của cạnh (đường đi) từ node hiện tại đến node kết thúc, sau đó trả về final path 
                # và tổng chi phí (path_cost). Nếu không thì tiếp tục
                if next_node == start and path.len == 8:
                    path.append(next_node)
                    path_cost += graph[current_node][next_node]["weight"]
                    return path, path_cost
                # tính chi phí của path mới nếu node tiếp theo được thêm vào
                new_path_cost = path_cost + graph[current_node][next_node]["weight"]
                # kiểm tra nếu chi phí của path mới thấp hơn chi phí path hiện tại, hoặc nếu một số ngẫu nhiên từ 0 
                # đến 1 nhỏ hơn xác suất chấp nhận giải pháp tệ hơn xác định bởi temp và sự khác biệt giữa chi phí path mới 
                # và chi phí path hiện tại
                if new_path_cost < path_cost or random.uniform(0, 1) < math.exp((path_cost - new_path_cost) / temperature):
                    # nếu chấp nhận thì thêm node tiếp theo vào path
                    path.append(next_node)
                    # nếu chấp nhận thì cập nhập chi phí path và node hiện tại mới
                    path_cost = new_path_cost
                    current_node = next_node
            # cập nhập nhiệt độ mới
            temperature *= 1 - cooling_rate
        path.append(start)
        # trả về path cuối cùng và tổng chi phí khi vòng lặp kết thúc
        path_cost = path_cost + graph[current_node][start]["weight"]
        return path, path_cost

    def start_algorithm(self):
        # lấy node bắt đầu từ box node bắt đầu
        start_node = self.start_node_combo_box.currentText()
        # chạy thuật toán SA với graph, node bắt đầu, node kết thúc; từ đó hiện path và tính toán tổng chi phí
        self.path, self.path_cost = self.simulated_annealing(self.graph, start_node)
        # set node hiện tại làm node bắt đầu
        self.current_node = start_node
        # vẽ đồ thị với path mới
        self.draw_graph()
        # set label thành "Tổng chi phí: " và tổng chi phí tính được
        self.total_cost_label.setText("Tổng chi phí: " + str(self.path_cost))

    def draw_graph(self):
      # set vị trí các nút bằng thuật toán spring layout
      pos = nx.spring_layout(self.graph)
      # set label cạnh từ graph
      edge_labels = nx.get_edge_attributes(self.graph, "weight")
      # vẽ các node với màu sắc và kích thước tương ứng
      nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=500)
      # set font chữ và size chữ cho label
      nx.draw_networkx_labels(self.graph, pos, font_size=14, font_family="consolas")
      # vẽ các cạnh
      nx.draw_networkx_edges(self.graph, pos)
      # set size chữ và font chữ tương ứng cho label cạnh
      nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=12, font_color="red")
      # tạo vòng lặp để vẽ các cạnh của path hiện tại với màu và độ rộng tương ứng
      for i in range(len(self.path) - 1):
          nx.draw_networkx_edges(self.graph, pos, edgelist=[(self.path[i], self.path[i + 1])],
                                edge_color="blue", width=2.0)
      # tắt đường trục để giúp graph tối giản hơn
      plt.axis("off")
      # hiển thị graph cuối cùng lên màn hình
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