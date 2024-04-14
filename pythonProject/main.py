from itertools import product

class Farm:
    def __init__(self, grid, seeds):
        self.grid = grid
        self.seeds = seeds

class Seed:
    def __init__(self, seed_id, cost, profit, bonuses):
        self.seed_id = seed_id
        self.cost = cost
        self.profit = profit
        self.bonuses = bonuses

def calculate_profit(grid, seed_properties, x, y, seed_id):
    seed = seed_properties[seed_id]
    profit = seed.profit - seed.cost  # Subtract the cost of planting the seed

    # Directions to check adjacent cells (up, down, left, right)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            adjacent = grid[ny][nx]
            if adjacent == '.':
                profit += seed.bonuses[0]  # Empty space bonus
            elif adjacent == '#':
                profit += seed.bonuses[1]  # Obstacle bonus
            elif adjacent.isalpha():  # Adjacent seed bonuses
                adj_seed = seed_properties[adjacent.upper()]
                index = 2 + ord(adjacent.upper()) - ord('A')
                profit += seed.bonuses[index] if index < len(seed.bonuses) else 0

    return profit

def place_seeds(grid, seed_properties):
    optimal_grid = [list(row) for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.' or grid[y][x].isalpha():
                best_profit = float('-inf')
                best_seed_id = None
                for seed_id, seed in seed_properties.items():
                    current_profit = calculate_profit(optimal_grid, seed_properties, x, y, seed_id)
                    if current_profit > best_profit:
                        best_profit = current_profit
                        best_seed_id = seed_id

                if best_seed_id:
                    optimal_grid[y][x] = best_seed_id.upper()

    return [''.join(row) for row in optimal_grid]

def parse_scenario(data):
    lines = data.strip().split("\n")
    grid_size_x, grid_size_y, num_seeds = map(int, lines[0].split())
    grid = lines[1:1 + grid_size_y]
    seeds_info = {}
    seed_lines_start = 1 + grid_size_y

    for i in range(num_seeds):
        parts = lines[seed_lines_start + i].split()
        seed_id, cost, profit = parts[0], int(parts[1]), int(parts[2])
        bonuses = [int(b) for b in parts[3:]]
        seeds_info[seed_id] = Seed(seed_id, cost, profit, bonuses)

    return Farm(grid, seeds_info)

def parse_input(input_text):
    lines = input_text.strip().split("\n")
    num_scenarios = int(lines[0])
    scenarios = []
    current_line = 1

    for _ in range(num_scenarios):
        gx, gy, ns = map(int, lines[current_line].split())
        scenario_length = 1 + gy + ns
        scenario_data = "\n".join(lines[current_line:current_line + scenario_length])
        scenarios.append(parse_scenario(scenario_data))
        current_line += scenario_length

    return scenarios

def main(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        input_text = f.read()

    scenarios = parse_input(input_text)

    with open(output_filename, 'w') as f:
        f.write(str(len(scenarios)) + "\n")
        for scenario in scenarios:
            seed_properties = {seed.seed_id: seed for seed in scenario.seeds.values()}
            placed_grid = place_seeds(scenario.grid, seed_properties)
            f.write("\n".join(placed_grid) + "\n")

if __name__ == '__main__':
    main("sample.in", "sample.txt")