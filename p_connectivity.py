import networkx as nx
from itertools import chain, combinations

from typing import Callable
from typing import Tuple
from collections.abc import Iterable

def powerset(iterable: Iterable) -> Iterable:
    """Return a generator for the powerset of an iterable"""
    s = list(iterable)
    return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))

# NOTE: connectivity functions are writen to find minimums
#       to find maximums a reverse iterator for the powerset would be needed

def component_p_edge_connectivity(g: nx.Graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    Find the minimum number of edges to remove so that some component of
    g no longer satisfies has_property

    g -- graph
    has_property -- function that returns true if a component has property
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

def component_p_vertex_connectivity(g: nx.graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    Finds the minimum number of verticies to remove so that some component of
    g no longer satisfies has_property

    g -- graph
    has_property -- function that returns true if a component has property
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

def p_edge_connectivity(g: nx.Graph, has_property: Callable) -> tuple :
    """
    Finds the minimum number of edges to remove so that
    g no longer satisfies has_property
    """
    for edge_removal_set in powerset(g.edges()):
        g_prime = g.copy()
        g_prime.remove_edges_from(edge_removal_set)
        if not has_property(g_prime):
            return edge_removal_set

    raise "Graph with no edges has property"

def p_vertex_connectivity(g: nx.Graph, has_property: Callable) -> tuple:
    """
    Finds the minimum number of verticies to remove so that
    g no longer satisfies has_property
    """
    for vertex_removal_set in powerset(g.edges()):
        g_prime = g.copy()
        g_prime.remove_nodes_from(vertex_removal_set)
        if not has_property(g_prime):
            return vertex_removal_set
