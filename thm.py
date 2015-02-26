import sys

N = -1

G = None
H = None
vis = None
vis_aux = None
valence = None

flows = {}

answer = []

allowed_flows = {
	3 : [-1, 1],
	4 : [-1, 1, 2],
	5 : [-1, 1, 2, -2]
}

def has_k_flow (graph):
	global N, G, H, vis, valence, flows

	G = graph
	N = len(G)

	H = [[0] * N for i in xrange(0, N)]
	vis = [False] * N
	valence = [0] * N

	for v in xrange(0, N):
		valence[v] = len(G[v])

		if valence[v] not in flows and valence[v] != 0:
			flows[valence[v]] = getWeights(valence[v])

	for v in xrange(0, N):
		G[v] = sorted(G[v], key=lambda u : valence[u], reverse=True)

	del answer[:]

	v = find_next()

	return dfs(v)


def getWeights (VALENCE, e = 0):
	global answer, E, edges

	if e == 0:
		del answer[:]
		edges = [0] * VALENCE

	elif e >= VALENCE:
		return None

	isLast = (e == (VALENCE - 1))

	weight2 = [0, 2]

	for w in xrange(0, 2):
		edges[e] = weight2[w]
		getWeights(VALENCE, e + 1)

		if isLast:
			edges2 = sum(edges) / 2

			if (VALENCE - edges2) % 2 == 0 and not (edges2 == VALENCE and edges2 % 2 != 0):
				answer.append(edges[:])

	if e == 0:
		return answer[:]

def find_next ():
	vertices = xrange(0, N)
	vertices = filter(lambda v : not vis[v], vertices)
	# pick most constrained variable
	vertices = sorted(vertices, key=lambda v : valence[v], reverse=True)

	return vertices.pop(0)

def dfs (v = 0):
	vis[v] = True

	if valence[v] == 0:
		sys.stderr.write ('error: vertex "%d" is 0-valent. Have you forgotten it?\n' % v)
		exit(1)

	constraints, neighbours = getConstraints(v)
	weights = flows[valence[v]]

	W = select(constraints, weights, v)
	isLast = (sum(vis) == N)

	if len(W) == 0:
		vis[v] = False
		return False

	for w in W:
		clear(v, neighbours)
		assign(v, w)

		counter = 0

		for u in G[v]:
			if not vis[u]:
				counter += 1

				if dfs(u):
					return True
				else:
					break

		deadlock = (not isLast and counter == 0)

		if deadlock and dfs(find_next()):
			return True

		elif isLast and checkEulerian():
			answer.append(H[:][:])
			return True


	vis[v] = False
	clear(v, neighbours)

	return False

def dfs_check(v, one_vertex, component, path):
	global vis_aux

	vis_aux[v] = component
	path.append(v)

	recursive_ones = 0

	for u in G[v]:
		if vis_aux[u] == 0 and H[v][u] == 0:
			recursive_ones += dfs_check(u, one_vertex, component, path)

	return int(one_vertex[v]) + recursive_ones

def checkEulerian():
	global vis_aux

	# for v in xrange(0, N):
	# 	weight2 = sum(H[v]) / 2

	# 	if (valence[v] - weight2) % 2 != 0:
	# 		return False


	vis_aux = [False] * N
	one_vertex = [(sum(H[v]) / 2) % 2 != 0 for v in xrange(0, N)]

	components = 0
	result = True
	paths = {}

	for v in xrange(0, N):
		if vis_aux[v] == 0:
			components += 1
			path = []

			C_ones = dfs_check(v, one_vertex, components, path)
			paths[components] = path

			if C_ones % 2 != 0:
				result = False 

	if result and False:
		for i in xrange(0, components):
			print i + 1, paths[i + 1]


	return result

def getConstraints (v):
	constraints = {}
	neighbours = []
	i = 0

	for u in G[v]:
		if H[v][u] != 0 or H[u][v] != 0:
			constraints[i] = 2
			neighbours.append(u)
		i += 1

	return constraints, neighbours


def select (constraints, possibilities, v):
	r = []

	for p in possibilities:
		for field in constraints:
			if p[field] != constraints[field]:
				break
		else:
			r.append(p[:])

	def valid (vector):
		for i in xrange(0, len(vector)):
			if vis[G[v][i]] and vector[i] == 2 and i not in constraints:
				return False
		return True

	return [i for i in r if valid(i)]

def assign (v, weights):
	for u in G[v]:
		w = weights.pop(0)
		H[u][v] = H[v][u] = w

def clear (v, neighbours):
	for u in G[v]:
		if u not in neighbours:
			H[u][v] = H[v][u] = 0