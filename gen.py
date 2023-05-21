import random
import networkx as nx
import matplotlib.pyplot as plt

class Functions():
	def __init__(self, graph, upa_graph, er_graph):
		self.graph = graph
		self.upa_graph = upa_graph
		self.er_graph = er_graph

	def draw(self):
		# Граф компьютерной сети
		res_net = self.compute_resilience(self.graph, self.random_order(self.graph))
		plt.plot(res_net, label='Computer network')

		# ER граф
		res_er = self.compute_resilience(self.er_graph, self.random_order(self.er_graph))
		plt.plot(res_er, label='ER graph')

		# UPA граф
		res_upa = self.compute_resilience(self.upa_graph, self.random_order(self.upa_graph))
		plt.plot(res_upa, label='UPA graph')

		plt.legend()
		plt.xlabel('Number of nodes removed')
		plt.ylabel('Size of largest component')
		plt.title('Resilience of computer network and random graphs')
		plt.show()

	def fast_targeted_order(self, who='UPA'):
		G = self.upa_graph if who == 'UPA' else self.er_graph if who == 'ER' else self.graph
		order = []
		while G:
			max_degree = max(dict(G.degree()).items(), key=lambda x: x[1])[0] # ищем вершину максимальной степени
			G.remove_node(max_degree) # удаляем эту вершину
			order.append(max_degree) # добавляем ее в порядок удаления
		return order[::-1] # переворачиваем список, чтобы порядок был правильный

	def targeted_order(self, who='UPA'):
		G = self.upa_graph if who == 'UPA' else self.er_graph if who == 'ER' else self.graph
		order = []
		degree_sets = [set() for _ in range(len(G))] # создаем список множеств для каждой степени
		for vertex, degree in dict(G.degree()).items():
			degree_sets[degree].add(vertex)
		for k in range(len(G) - 1, -1, -1): # перебираем все степени в порядке убывания
			while degree_sets[k]: # пока множество не пусто
				vertex = degree_sets[k].pop() # извлекаем вершину
				for neighbor in G.neighbors(vertex): # удаляем вершину и соединения с соседями
					try:
						neighbor_degree = G.degree(neighbor)
						degree_sets[neighbor_degree].remove(neighbor)
						degree_sets[neighbor_degree - 1].add(neighbor)
					except:
						pass
				degree_sets.pop(k)
				G.remove_node(vertex)
				order.append(vertex)
		return order


	def compute_resilience(self, g, attack_order):
		"""
		Функция вычисления устойчивости графа.
		Аргументы:
		g - граф NetworkX
		attack_order - список вершин для удаления в порядке атаки
		Возвращает список значений связности графа после каждого шага атаки
		"""
		# Создаем копию исходного графа
		G = g.copy()

		# Вычисляем начальную связность графа
		initial_components = sorted(nx.connected_components(G), key=len, reverse=True)
		resilience = [len(initial_components)]

		# Удаляем вершины и вычисляем связность графа после каждого шага атаки
		for node in attack_order:
			try:
				G.remove_node(node)
				components = sorted(nx.connected_components(G), key=len, reverse=True)
				resilience.append(len(components))
			except:
				pass

		return resilience

	def random_order(self, g):
		nodes = list(g.nodes())
		random.shuffle(nodes)
		return nodes

class Gen():
	def __init__(self):
		pass

	def load_graph(self, filename):
		G = nx.Graph()

		# Открываем файл и добавляем ребра в граф
		with open(filename, 'r') as f:
			for line in f:
				nodes = line.strip().split()
				src = nodes[0]
				for dst in nodes[1:]:
					G.add_edge(src, dst)

		return G

	def ER(self, n, p):
		"""
		Случайный ER граф

		:param n: – количество вершин в графе
		:param p: – вероятность того, что произвольное ребро (i,j) будет добавлено в граф
		:return: - граф
		"""
		return nx.erdos_renyi_graph(n, p)

	def nx_UPA(self, n, m=2):
		UPA_graph = nx.barabasi_albert_graph(n, m)
		m = sum(dict(UPA_graph.degree()).values()) / len(UPA_graph)

		return UPA_graph, m

	def DPA(self, n, k):
		"""
		Случайный DPA граф

		:param n: – количество вершин в графе
		:param m: – количество соседей
		:return: - граф
		"""


		graph = [[0 for i in range(n)] for j in range(n)]
		vertices = [i for i in range(m) for j in range(m)]
		edges = [i for i in range(m) for j in range(i)]
		for i in range(m):
			for j in range(m):
				if i != j:
					graph[i][j] = 1
					graph[j][i] = 1
		for i in range(m, n):
			selected_vertices = random.choices(vertices, weights=edges, k=m)
			new_vertex = [0]*n
			for j in selected_vertices:
				new_vertex[j] = 1
			new_edges = [j for j in selected_vertices for k in range(edges[j])]
			vertices.append(i)
			edges.append(len(new_edges) + 1)
			for j in range(i):
				if new_vertex[j]:
					graph[j][i] = 1
					graph[i][j] = 1
					edges[j] += 1
					edges[i] += 1
			edges[i] = len(new_edges)
			edges += new_edges
		return graph