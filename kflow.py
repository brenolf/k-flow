N = -1

G = None
H = None
vis = None
valence = None

KFLOW = 4
flows = {}

answer = []

allowed_flows = {
	3 : [-1, 1],
	4 : [-1, 1, 2],
	5 : [-1, 1, 2, -2]
}

def has_k_flow (k_flow, graph):
	global KFLOW, N, G, H, vis, valence, flows

	G = graph
	KFLOW = k_flow
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

	for w in xrange(0, KFLOW - 1):
		edges[e] = allowed_flows[KFLOW][w]
		getWeights(VALENCE, e + 1)

		if isLast and (sum(edges) % KFLOW == 0):
			answer.append(edges[:])

	if e == 0:
		return answer[:]

def fftv (w): #Four-flow 2-valent
	return w == 2 and KFLOW == 4

def find_next ():
	vertices = xrange(0, N)
	vertices = filter(lambda v : not vis[v], vertices)
	# pick most constrained variable
	vertices = sorted(vertices, key=lambda v : valence[v], reverse=True)

	return vertices.pop(0)

def dfs (v = 0):
	vis[v] = True

	constraints, neighbours = getConstraints(v)
	weights = flows[valence[v]]

	W = select(constraints, weights)
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

		elif isLast:
			answer.append(H[:][:])
			return True


	vis[v] = False
	clear(v, neighbours)

	return isLast

def getConstraints (v):
	constraints = {}
	neighbours = []
	i = 0

	for u in G[v]:
		if H[v][u] != 0 or H[u][v] != 0:
			constraints[i] = H[v][u] if H[v][u] != 0 else -H[u][v]
			neighbours.append(u)
		i += 1

	return constraints, neighbours


def select (constraints, possibilities):
	r = []

	for p in possibilities:
		for field in constraints:
			if p[field] != constraints[field]:
				break
		else:
			r.append(p[:])

	return r

def assign (v, weights):
	for u in G[v]:
		w = weights.pop(0)

		if fftv(w):
			H[u][v] = H[v][u] = w

		elif w < 0:
			H[u][v] = -w

		else:
			H[v][u] = w

def clear (v, neighbours):
	for u in G[v]:
		if u not in neighbours:
			H[u][v] = H[v][u] = 0
