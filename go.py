import kflow
import fileinput
import string
import sys

N = -1
M = -1
G = None
KFLOW = 4

for line in fileinput.input():

	if line != '\n':
		u, v = string.split(line)
		u, v = int(u), int(v)

		if G is None:
			N, M = u, v
			G = [[] * N for i in xrange(0, N)]

		else:
			G[u].append(v)
			G[v].append(u)

print kflow.has_k_flow(KFLOW, G)