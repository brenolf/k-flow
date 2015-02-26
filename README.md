# _k_-flow Tester

A python program to test whether a graph has a k-flow or not.

## Introduction

Let  `k >  1`  be an  integer,  let `G`  be  a graph,  let  `D` be  an orientation  of  `G` and  let  `phi`  be  a weight  function  that associates to each edge of `G` a  positive integer in the set `{1, 2, ...,  k - 1}`. The  pair  `(D, phi)`  is a  _(nowhere-zero) k-flow_  of `G`  if  the sum of the weights of  all edges leaving every  vertex `v` of `G` equals the sum of the weights of all edges entering `v`, and we call `v` _balanced_. Similarly, we say the  pair  `(D, phi)`  is a  _(nowhere-zero) modular-k-flow_, if every vertex `v` is balanced modulus `k`.

Tutte [1]  defined   the   concept  of   _k_-flows   as   a generalization of  the concept of _k_-face-colourings  after observing that,  for  any planar  graph,  a  _k_-flow  can  be obtained  from _k_-face-colouring   and   vice-versa. Tutte  proposed three celebrated conjectures  regarding _k_-flows of graphs, known as the 5-, 4- and 3-Flow Conjectures.

[1] W. T. Tutte. A contribution to the theory of chromatic polynomials. Can. J. Math., 6:80–91, 1954.

## Usage

One may use `kflow.py` as a standalone library. Its main function (and actually the only one which should be called by the client-side) is `has_k_flow` which takes as its two mandatory arguments the number `k` representing which of the flows (3, 4, 5 should be used and a graph `G` represented by an adjacency list. The function returns a boolean value that is `True` if the graph admits a modular-_k_-flow. If there is a flow, it is accessible through `kflow.answer`, which is a list of possibles _k_-flows found; However, as a current limitation, if there is a modular-_k_-flow, `kflow.answer` will only have the first found _k_-flow.

The file `go.py` is an example of how to read a graph from input and use the _k-flow_ library.

## 4-flow

The `thm.py` library was developed exclusively for 4-flows. Its main function is the same as the `kflow.py` function; However, one should call `thm.has_k_flow` instead. It works by identifying set of edges in the graph that could be used as weight 2 edges, such that their removal yields an Eulerian graph. It is exponentially faster than the brute-force approach, but still not extremely fast.
