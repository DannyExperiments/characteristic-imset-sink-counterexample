# Problem and proof

A sink rewrite reverses the outgoing arcs at a specified vertex and preserves every other arc. The question asks whether the resulting segment between distinct characteristic imsets is an edge of the fixed-skeleton characteristic imset polytope. [Source, Conjecture 1](https://arxiv.org/pdf/2302.03647v2#page=11)

Use skeleton edges 01, 02, 03, 04, 12, 13. Orient from earlier to later.

| DAG | Order | Extra imset coordinates |
| --- | --- | --- |
| D | 4, 2, 0, 3, 1 | 123, 0123, 024 |
| T | 4, 0, 3, 1, 2 | none |
| U | 4, 0, 3, 2, 1 | 123, 0123 |
| V | 4, 2, 0, 1, 3 | 024 |

For every DAG the six pair coordinates and the triples 012, 013 are 1. All coordinates beyond these and the indicated extras vanish. A coordinate is on exactly when some vertex in its set has all others as parents. The sink at 2 sends D to T. The four distinct binary vectors satisfy $c_D+c_T=c_U+c_V$. A face containing the midpoint would also contain the latter two vertices, which cannot lie on the segment between the former two. Thus the segment is not an edge.

Adding vertices ordered after the old five leaves the old coordinates intact and makes all new coordinates common to the four imsets. If vertex 2 gains no neighbor, the same sink rewrite produces T. Attaching leaves to vertex 4 makes a connected example at any larger order.

For each labeled skeleton through four vertices, enumerate all topological orders and move each vertex to the end. On each affected pair, fix coordinates where its endpoints agree to form a face. Exact integer weights identify the two endpoints as the sole maximizing vertices in this face. The pair is then an edge in the face and the full fixed-skeleton polytope. See the paper for formal details and how the finite computation is exhausted. [Paper](../paper/manuscript.pdf) · [Replay](../REPRODUCIBILITY.md)
