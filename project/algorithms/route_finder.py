import heapq
import math

def heuristic(node, goal):
    """Simple heuristic function (can be enhanced with actual coordinates)"""
    distances = {
        ("ER", "ICU"): 5,
        ("ER", "Ward"): 8,
        ("ER", "Lab"): 10,
        ("ICU", "Ward"): 6,
        ("ICU", "Lab"): 4,
        ("Ward", "Lab"): 2,
    }
    
    if (node, goal) in distances:
        return distances[(node, goal)]
    elif (goal, node) in distances:
        return distances[(goal, node)]
    return 0

def a_star(graph, start, goal):
    """
    A* search algorithm for finding optimal route.
    
    graph structure:
    {
        "ER": [("ICU", 5), ("Ward", 8)],
        "ICU": [("ER", 5), ("Lab", 4)],
        ...
    }
    """
    
    open_set = []
    heapq.heappush(open_set, (0, 0, start, []))
    
    g_scores = {start: 0}
    visited = set()
    
    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)
        
        if current in visited:
            continue
            
        visited.add(current)
        current_path = path + [current]
        
        if current == goal:
            return current_path, g_score
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
                
            tentative_g = g_score + weight
            
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, 
                             (f_score, tentative_g, neighbor, current_path))
    
    return None, float("inf")

def get_all_routes(graph, start, goal):
    """Get all possible routes (for comparison)"""
    def dfs(current, path, visited, weight):
        if current == goal:
            return [(path + [current], weight)]
        
        routes = []
        visited.add(current)
        
        for neighbor, w in graph.get(current, []):
            if neighbor not in visited:
                new_routes = dfs(neighbor, path + [current], 
                               visited.copy(), weight + w)
                routes.extend(new_routes)
        
        return routes
    
    all_routes = dfs(start, [], set(), 0)
    return sorted(all_routes, key=lambda x: x[1])  # Sort by cost