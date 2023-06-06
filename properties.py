"""
Properties for Network Connectivity

functions:
    circumference
    has_l_circ
"""
from typing import Callable
import networkx as nx
from networkx import is_planar # add to namespace

def circumference(g: nx.Graph) -> int:
    """
    Compute the cicumference of a graph, 0 if acyclic
    """
    cycles = list(nx.algorithms.cycles.simple_cycles(g))
    cycle_sizes = sorted(cycles, key = lambda s : len(s))
    return len(cycle_sizes[-1]) if len(cycle_sizes) else 0

def _has_l_circ(g: nx.Graph, l: int) -> bool:
    """
    Checks of a graph has at least circumference l
    """
    return circumference(g) >= l

def has_l_circ(l: int) -> Callable:
    """
    Anonymous function generator for _has_l_circ
    """
    return lambda g : _has_l_circ(g, l)
