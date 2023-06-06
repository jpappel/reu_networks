"""
Functions for working with connectivity properties on networks

functions:
    powerset
    component_p_edge_connectivity
    component_p_vertex_connectivity
    p_edge_connectivity
    p_vertex_connectivity
"""
from typing import Callable
from typing import Tuple
from collections.abc import Iterable
from itertools import chain, combinations

import networkx as nx


def powerset(iterable: Iterable) -> Iterable:
    """Return a generator for the powerset of an iterable"""
    s = list(iterable)
    return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))

# NOTE: connectivity functions are writen to find minimums
#       to find maximums a reverse iterator for the powerset would be needed

# NOTE: for some graph classes their exist much better algorithims
#       to speed up or skip isomorphism comparision

def component_p_edge_connectivity(g: nx.Graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    Find the minimum number of edges to remove so that some component of
    g no longer satisfies has_property

    g -- graph
    has_property -- function that returns true if a component has property
    """
    memo = [ [] for _ in range(g.size())]
    for edge_removal_set in powerset(g.edges()):
        g_prime = g.copy()
        g_prime.remove_edges_from(edge_removal_set)
        if any(nx.is_isomorphic(g_prime, g_memo) for g_memo in memo[len(edge_removal_set)]):
            continue
        memo[len(edge_removal_set)].append(g_prime.copy())
        component_has_property = []
        for component_verts in nx.components.connected_components(g_prime):
            component = g_prime.subgraph(component_verts)
            component_has_property.append(has_property(component))
        if not all(component_has_property):
            return edge_removal_set, component_has_property

    raise Warning("Graph with no edges has property")

def component_p_vertex_connectivity(g: nx.Graph, has_property: Callable) -> Tuple[tuple,list] :
    """
    Finds the minimum number of verticies to remove so that some component of
    g no longer satisfies has_property

    g -- graph
    has_property -- function that returns true if a component has property
    """
    memo = [ [] for _ in range(g.order())]
    for vertex_removal_set in powerset(g.nodes()):
        g_prime = g.copy()
        g_prime.remove_nodes_from(vertex_removal_set)
        if any(nx.is_isomorphic(g_prime, g_memo) for g_memo in memo[len(vertex_removal_set)]):
            continue
        memo[len(vertex_removal_set)].append(g_prime.copy())
        # TODO: redundant
        component_has_property = []
        for component_verts in nx.components.connected_components(g_prime):
            component = g_prime.subgraph(component_verts)
            component_has_property.append(has_property(component))
        if not all(component_has_property):
            return vertex_removal_set, component_has_property

    raise Warning("Graph with no verticies has property")

def p_edge_connectivity(g: nx.Graph, has_property: Callable) -> tuple :
    """
    Finds the minimum number of edges to remove so that
    g no longer satisfies has_property
    """
    memo = [ [] for _ in range(g.size())]
    for edge_removal_set in powerset(g.edges()):
        g_prime = g.copy()
        g_prime.remove_edges_from(edge_removal_set)
        if any( nx.is_isomorphic(g_prime, g_memo) for g_memo in memo[len(edge_removal_set)]):
            continue
        memo[len(edge_removal_set)].append(g_prime.copy())
        if not has_property(g_prime):
            return edge_removal_set

    raise Warning("Graph with no edges has property")

def p_vertex_connectivity(g: nx.Graph, has_property: Callable) -> tuple:
    """
    Finds the minimum number of verticies to remove so that
    g no longer satisfies has_property
    """
    memo = [ [] for _ in range(g.order())]
    for vertex_removal_set in powerset(g.nodes()):
        g_prime = g.copy()
        g_prime.remove_nodes_from(vertex_removal_set)
        if any(nx.is_isomorphic(g_prime, g_memo) for g_memo in memo[len(vertex_removal_set)]):
            continue
        memo[len(vertex_removal_set)].append(g_prime.copy())
        if not has_property(g_prime):
            return vertex_removal_set

    raise Warning("Graph with no verticies has property")
