import networkx as nx
from itertools import chain, combinations

from typing import Callable
from typing import Tuple
from collections.abc import Iterable

def powerset(iterable: Iterable) -> Iterable:
    s = list(iterable)
    return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))

def p_edge_connectivity(g: nx.Graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    TODO: Documentation
    """
    for edge_removal_set in powerset(g.edges()):
        g_prime = g.copy()
        g_prime.remove_edges_from(edge_removal_set)
        component_has_property = []
        for component_verts in nx.components.connected_components(g_prime):
            component = g_prime.subgraph(component_verts)
            component_has_property.append(has_property(component))
        if not all(component_has_property):
            return edge_removal_set, component_has_property

    raise "Graph with no edges has property"

def p_vertex_connectivity(g: nx.graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    TODO: Documentation
    """
    for vertex_removal_set in powerset(g.nodes()):
        g_prime = g.copy()
        g_prime.remove_nodes_from(vertex_removal_set)
        # TODO: redundant
        component_has_property = []
        for component_verts in nx.components.connected_components(g_prime):
            component = g_prime.subgraph(component_verts)
            component_has_property.append(has_property(component))
        if not all(component_has_property):
            return edge_removal_set, component_has_property

    raise "Graph with no verticies has property"

