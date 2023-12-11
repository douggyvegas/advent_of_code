import time
import re

def main():
    with open("09.in") as iteration_line:
        scenarios = [ ]
        for line in iteration_line.read().splitlines():
            scenario = [ [ int(s) for s in re.findall(r'-?\d+', line)] ]
            iteration = 0
            while not all(n == 0 for n in scenario[iteration]):
                next_numbers = [ ]
                for i in range(len(scenario[iteration]) - 1):
                    next_numbers.append(scenario[iteration][i+1] - scenario[iteration][i])
                iteration += 1
                scenario.append(next_numbers)
            scenarios.append(scenario)

        for scenario in scenarios:
            scenario[-1].insert(0, 0)
            scenario[-1].append(0)
            for iteration in range(1, len(scenario)):
                scenario[len(scenario) - iteration - 1].insert(0, scenario[len(scenario) - iteration - 1][0] - scenario[len(scenario) - iteration][0])
                scenario[len(scenario) - iteration - 1].append(scenario[len(scenario) - iteration - 1][-1] + scenario[len(scenario) - iteration][-1])

        for scenario in scenarios:
            print("-------------------------------------------------------------")
            for i, l in enumerate(scenario):
                print(''.join("  "*i) + f"{l}")
        
        print(f"part 1: {sum([ scenario[0][-1] for scenario in scenarios ])}")
        print(f"part 2: {sum([ scenario[0][0] for scenario in scenarios ])}")




start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")