import heapq
import itertools

class RouteOptimizer:
    def __init__(self):
        # Locations represented as (x, y) coordinates
        self.locations = {
            'Depot': (0, 0),
            'Point_A': (2, 3),
            'Point_B': (5, 1),
            'Point_C': (1, 7),
            'Point_D': (4, 4)
        }
        # Traffic multiplier (1.0 = clear, 2.0 = heavy traffic)
        self.traffic_conditions = {
            ('Depot', 'Point_A'): 1.2,
            ('Point_A', 'Point_C'): 2.5,
            ('Point_C', 'Point_D'): 1.1,
            ('Point_D', 'Point_B'): 1.8,
        }
        # Delivery Priority (Lower number = Higher priority)
        self.priorities = {
            'Point_A': 2,
            'Point_B': 1,
            'Point_C': 3,
            'Point_D': 1
        }

    def calculate_distance(self, loc1, loc2):
        p1, p2 = self.locations[loc1], self.locations[loc2]
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def get_travel_cost(self, start, end):
        dist = self.calculate_distance(start, end)
        traffic = self.traffic_conditions.get((start, end), 1.0)
        # Fuel consumption/time factor weighted by traffic and priority
        priority_weight = self.priorities.get(end, 5) 
        return dist * traffic * (priority_weight * 0.5)

    def optimize_route(self):
        stops = [loc for loc in self.locations.keys() if loc != 'Depot']
        best_route = None
        min_cost = float('inf')

        # Solving as a Weighted Traveling Salesperson Problem (Brute Force for small sets)
        for permutation in itertools.permutations(stops):
            current_route = ('Depot',) + permutation + ('Depot',)
            current_cost = 0
            
            for i in range(len(current_route) - 1):
                current_cost += self.get_travel_cost(current_route[i], current_route[i+1])
            
            if current_cost < min_cost:
                min_cost = current_cost
                best_route = current_route

        return best_route, min_cost

def main():
    optimizer = RouteOptimizer()
    route, cost = optimizer.optimize_route()
    
    print("--- Fleet Route Optimization System ---")
    print(f"Optimal Delivery Sequence: {' -> '.join(route)}")
    print(f"Calculated Efficiency Score (Lower is better): {cost:.2f}")

if __name__ == "__main__":
    main()