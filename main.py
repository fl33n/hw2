import random, time
import networkx as nx
from gen import Functions, Gen
import matplotlib.pyplot as plt


gen = Gen()


############################################


g = gen.load_graph('alg_rf7.txt')

n = g.number_of_nodes()
m = g.number_of_edges()
p = m / (n*(n-1)/2)

upa_graph, m_upa = gen.nx_UPA(n)
er_graph = nx.erdos_renyi_graph(n, p)

print(n, m)
print(p, m_upa)

degrees = [degree for _, degree in upa_graph.degree()]
upa_graph = nx.configuration_model(degrees)
upa_graph = nx.Graph(upa_graph)
upa_graph.remove_edges_from(nx.selfloop_edges(upa_graph))


func = Functions(g, upa_graph, er_graph)


############### ПОДЗАДАЧА №2 ###############


def task_2():
	global func, gen
	global g, upa_graph, er_graph
	global n, m, p, m_upa

	func.draw()


############### ПОДЗАДАЧА №3 ###############


def task_3():
	global func, gen
	global g, upa_graph, er_graph
	global n, m, p, m_upa

	k = int(0.2 * n)
	nodes_to_remove = list(g.nodes())[:k]
	g.remove_nodes_from(nodes_to_remove)

	nodes_to_remove = list(upa_graph.nodes())[:k]
	upa_graph.remove_nodes_from(nodes_to_remove)

	nodes_to_remove = list(er_graph.nodes())[:k]
	er_graph.remove_nodes_from(nodes_to_remove)

	func = Functions(g, upa_graph, er_graph)
	func.draw()


############### ПОДЗАДАЧА №4 ###############


def task_4():
	global func, gen
	global g, upa_graph, er_graph
	global n, m, p, m_upa

	ns = range(10, 1000, 5)
	m = 5

	upa_graph, m_upa = gen.nx_UPA(n, m=m)
	degrees = [degree for _, degree in upa_graph.degree()]
	upa_graph = nx.configuration_model(degrees)
	upa_graph = nx.Graph(upa_graph)
	upa_graph.remove_edges_from(nx.selfloop_edges(upa_graph))
	
	func = Functions(g, upa_graph, er_graph)

	targeted_times = []
	fast_targeted_times = []
	for n in ns:
		start_time = time.time()
		func.targeted_order()
		targeted_times.append(time.time() - start_time)
		start_time = time.time()
		func.fast_targeted_order()
		fast_targeted_times.append(time.time() - start_time)

	plt.plot(ns, targeted_times, label='targeted_order')
	plt.plot(ns, fast_targeted_times, label='fast_targeted_order')
	plt.xlabel('n')
	plt.ylabel('time, s')
	plt.legend()
	plt.show()



############### ПОДЗАДАЧА №5 ###############


def task_5():
	global func, gen
	global g, upa_graph, er_graph
	global n, m, p, m_upa

	order1 = func.targeted_order("ER")
	order2 = func.targeted_order()
	order3 = func.targeted_order("NETWORK")

	# вычисление устойчивости при атаке узлов
	resilience1 = func.compute_resilience(er_graph, order1)
	resilience2 = func.compute_resilience(upa_graph, order2)
	resilience3 = func.compute_resilience(g, order3)

	# отображение на графике
	plt.plot(resilience1, label='ER graph')
	plt.plot(resilience2, label='UPA graph')
	plt.plot(resilience3, label='Citation graph')
	plt.legend()
	plt.title('Resilience of networks under node attack')
	plt.xlabel('Number of nodes removed')
	plt.ylabel('Size of largest connected component')
	plt.show()

############### MAIN ###############


if __name__ == "__main__":
	# task_2()
	# task_3()
	task_4()
	# task_5()