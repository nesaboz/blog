import heapq

class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:

        adj_list = defaultdict(list)
        for a,b,distance in roads:
            adj_list[a].append((distance, b))
            adj_list[b].append((distance, a))
        
        start = 1
        end = n
        pq = [(0, start)]

        distances = {i: math.inf for i in range(1, n+1)}  # distance from start to node i

        while pq:
            distance, node = heapq.heappop(pq)

            if distance > distances[node]:
                # we have already visited node before an were able to reach it in shorter distance
                continue
            else:
                distances[node] = distance

            if node == end:
                continue
            
            for weight, node2 in adj_list[node]:
                heapq.heappush(pq, distance + weight, node2))

        return distances[end]
