#to install pydot: pip install pydot
#to install graphviz https://www.graphviz.org/download/
import pydot

class CMyDot (object):

    def __init__(self, root_node): 

        self.graph = pydot.Dot("my_graph", graph_type="digraph")#, bgcolor="yellow")

        # Add nodes
        self.my_node = pydot.Node(root_node, label=root_node)
        self.graph.add_node(self.my_node)
        # Or, without using an intermediate variable:
        #graph.add_node(pydot.Node("b", shape="circle"))
        self.graph.write_png("graph.png")

    def plot_edge(self,edge_source,edge_destination ): 
 
        my_edge = pydot.Edge(edge_source, edge_destination, color="blue")
        self.graph.add_edge(my_edge)
        self.graph.write_png("graph.png")
   

