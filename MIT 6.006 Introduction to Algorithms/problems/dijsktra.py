"""
----Dijkstra----
Input: s
while not all explored:
    -extract min d[V]
    -relax

----BiDijskra----
Input: s and t

while not all explored or extract(S) != extract(T)
    -extract min from s side
    -relax

    -extract min from t (reversed)
    -relax

- find min sum (ds[x] + dt[x])
- reconstruct s->x and x->t

----Dijsktra potential----
- use path(u,v) = w(u,v) - lamda(u) + lambda(v)
- given lamda change weights with some insight

"""


"""
INPUT graph and weights
 ---->1--->
| 1   |  1 |
0     |1    2
| 3   |  2 |
 ---->3--->

"""

graph = {
    0: {1:1, 3:3},
    1: {2:1, 3:1},
    2: {},
    3: {2:2},
}

def reverse(graph):
    r_graph = {v:{} for v in graph}
    for head in graph:
        for tail in graph[head]:
            r_graph[tail][head] = graph[head][tail]
    return r_graph

import heapq
def dijkstra(graph, s, t):

    distance = dict()
    explored = set()
    parents = dict()
    heap = list()
    parents = {}

    heapq.heappush(heap, (0, s))

    while len(heap):
        #extract min
        weight, vertex = heapq.heappop(heap)

        #relax if not yet
        if vertex not in explored:
            explored.add(vertex)
            distance[vertex] = weight
            # early break
            # if vertex == t:
            #     break
            for tail in graph[vertex]:
                tail_distance = graph[vertex][tail] + weight
                if tail not in explored and distance.get(tail, float('inf')) > tail_distance:
                    distance[tail] = tail_distance
                    parents[tail] = vertex
                    heapq.heappush(heap, (tail_distance, tail))

    print("distance", distance[t])

    vertex = t
    while vertex != s:
        print(vertex)
        vertex = parents[vertex]



def bidijksta(graph, start, end):

    r_graph = reverse(graph)
    r_distances = dict()

    distances = dict()
    explored_foward = set()
    explored_back = set()

    heap_foward = [(0, start)]
    heap_back = [(0, end)]

    while len(heap_foward) and len(heap_back):

        weight, vertex = heapq.heappop(heap_foward)
        if vertex not in explored_foward:
            distances[vertex] = weight
            explored_foward.add(vertex)
            for tail in graph[vertex]:
                tail_distance = weight + graph[vertex][tail]
                if distances.get(tail, float('inf')) > tail_distance:
                    distances[tail] = tail_distance
                    heapq.heappush(heap_foward, (tail_distance, tail))

        weight, vertex = heapq.heappop(heap_back)
        if vertex not in explored_back:
            r_distances[vertex] = weight
            explored_back.add(vertex)

            for tail in r_graph[vertex]:
                tail_distance = weight + r_graph[vertex][tail]
                if r_distances.get(tail, float('inf')) > tail_distance:
                    r_distances[tail] = tail_distance
                    heapq.heappush(heap_back, (tail_distance, tail))

        if explored_foward.intersection(explored_back):
            print(explored_foward)
            print(explored_back)
            break

    # found min sum - equal to path
    # reconstruct after
    min_vertex = None
    min_value = float('inf')

    for v in graph:
        vertex_sum = distances.get(v, float('inf')) + r_distances.get(v, float('inf'))
        if vertex_sum < min_value:
            min_value = vertex_sum
            min_vertex = v
    print(min_vertex)
    print(min_value)




# dijkstra(graph, 0, 3)
# bidijksta(graph, 0, 3)

