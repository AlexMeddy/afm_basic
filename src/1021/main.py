from CEdge import CEdge
from CVertex import CVertex
from CGraph import CGraph

print("---------testing CGraph-----------")
graph_obj = CGraph("graph_A")
print("graph_obj.name = {}".format(graph_obj.name))
vertex_a_obj = CVertex("A")
vertex_b_obj = CVertex("B")
vertex_c_obj = CVertex("C")
vertex_d_obj = CVertex("D")
vertex_e_obj = CVertex("E")
graph_obj.vertex_list.append(vertex_a_obj)
graph_obj.vertex_list.append(vertex_b_obj)
graph_obj.vertex_list.append(vertex_c_obj)
graph_obj.vertex_list.append(vertex_d_obj)
graph_obj.vertex_list.append(vertex_e_obj)
for cn in graph_obj.vertex_list:
    print("vertex_list cn.name = {}".format(cn.name))
vertex_a_obj.edge_list.append(CEdge("AB", vertex_a_obj, vertex_b_obj))
vertex_a_obj.edge_list.append(CEdge("AD", vertex_a_obj, vertex_d_obj))
vertex_b_obj.edge_list.append(CEdge("BC", vertex_b_obj, vertex_c_obj))
graph_obj.vertex_list[1].edge_list.append(CEdge("BE", vertex_b_obj, vertex_e_obj))
vertex_d_obj.edge_list.append(CEdge("DA", vertex_d_obj, vertex_a_obj))
graph_obj.print_all_edges()

'''
print("----------testing CVertex------------")
vertex_obj = CVertex("C")
vertex_obj.edge_list.append(CEdge("AB", vertex_a_obj, vertex_b_obj))
vertex_obj.edge_list.append(CEdge("AD", vertex_a_obj, vertex_d_obj))
for cn in vertex_obj.edge_list:
    print("vertex_obj.name = {} edge_list cn.name = {} cn.vertex_a = {} cn.vertex_b = {}".format(vertex_obj.name, cn.name, cn.vertex_a.name, cn.vertex_b.name))
print("--------------testing CEdge------------")
edge_obj = CEdge("AB", CVertex("A"), CVertex("B"))
print("edge_obj.name = {} vertex_a.name = {} vertex_b.name = {}".format(edge_obj.name, edge_obj.vertex_a.name, edge_obj.vertex_b.name))
'''