#!/usr/bin/env python3
"""Exact midpoint, lifting examples, and exposing vectors for small sink moves."""
from collections import Counter
from itertools import combinations, permutations, product

EDGES = ((0,1), (0,2), (0,3), (0,4), (1,2), (1,3))
ORDERS = ((4,2,0,3,1), (4,0,3,1,2), (4,0,3,2,1), (4,2,0,1,3))


def orient(edges, order):
    rank = {vertex: i for i, vertex in enumerate(order)}
    return {(u,v) if rank[u] < rank[v] else (v,u) for u,v in edges}


def support(n, arcs):
    parents = [set() for _ in range(n)]
    for u,v in arcs:
        parents[v].add(u)
    return frozenset(tuple(sorted((v,*subset)))
        for v, prior in enumerate(parents) for k in range(1, len(prior) + 1)
        for subset in combinations(prior,k))


def put_sink(arcs, vertex):
    return {(v,u) if u == vertex else (u,v) for u,v in arcs}


def assert_witness(edges, orders):
    n = len(orders[0])
    assert all(sorted(o) == list(range(n)) for o in orders)
    graphs = [orient(edges,o) for o in orders]
    assert graphs[1] == put_sink(graphs[0],2)
    d,t,u,v = (support(n,g) for g in graphs)
    assert len({d,t,u,v}) == 4
    assert d & t == u & v
    assert d ^ t == u ^ v
    return d,t,u,v


def exposure_radius(a,b,imsets):
    difference = a ^ b
    coordinates = sorted(difference)
    other = [c for c in imsets if c not in (a,b) and c - difference == a - difference]

    for radius in range(4):
        for weights in product(range(-radius,radius + 1), repeat=len(coordinates)):
            def score(imset):
                return sum(weight for x,weight in zip(coordinates,weights) if x in imset)
            bound = score(a)
            if bound == score(b) and all(score(c) < bound for c in other):
                return radius
    raise AssertionError(f"No small exposing vector for {a} and {b}")


def certify_small(n):
    all_edges = tuple(combinations(range(n),2))
    orders = tuple(permutations(range(n)))
    changes = 0
    counts = Counter()
    for flags in product((0,1), repeat=len(all_edges)):
        edges = tuple(edge for edge,flag in zip(all_edges,flags) if flag)
        imset_at = {o:support(n,orient(edges,o)) for o in orders}
        imsets = set(imset_at.values())
        checked = set()
        for order,a in imset_at.items():
            arcs = orient(edges,order)
            for v in range(n):
                last = tuple(u for u in order if u != v) + (v,)
                assert orient(edges,last) == put_sink(arcs,v)
                b = imset_at[last]
                if a == b:
                    continue
                changes += 1
                pair = frozenset((a,b))
                if pair not in checked:
                    checked.add(pair)
                    counts[exposure_radius(a,b,imsets)] += 1
    return changes, dict(sorted(counts.items()))


def main():
    d,t,u,v = assert_witness(EDGES,ORDERS)
    assert [sorted(x - t) for x in (d,t,u,v)] == [
        [(0,1,2,3),(0,2,4),(1,2,3)], [], [(0,1,2,3),(1,2,3)], [(0,2,4)]]
    assert sorted(x for x in t if len(x) > 2) == [(0,1,2),(0,1,3)]
    print("PASS: four distinct imsets, exact sink rewrite, and coordinatewise midpoint")
    for n in range(6,15):
        edges = EDGES + tuple((4,v) for v in range(5,n))
        assert_witness(edges,[o + tuple(range(5,n)) for o in ORDERS])
    print("PASS: nine connected lifts from order 6 through order 14")
    expected = ((0,{}),(0,{}),(24,{0:3}),(2208,{0:156,1:12,2:30,3:4}))
    for n, reference in enumerate(expected,1):
        observed = certify_small(n)
        assert observed == reference
        print(f"n={n}: {observed[0]} changing moves, distinct pairs by exposing radius {observed[1]}")
    print("PASS: exact supporting vectors for all smaller sink pairs")


if __name__ == "__main__":
    main()
