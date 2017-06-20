from problem import *
import random

MAX_ITERATION = 50


class AntSystem:

    problem = None
    best_value = 0
    num_ant = 60
    pheromone = []
    best_solution_value = 0
    best_solution = None
    reset_best_solution_value = 0
    reset_best_solution = None

    rho = 0.15

    def __init__(self, problem):
        self.problem = problem
        self.pheromone = [0.5] * problem.total_nodes

    def calculate_gain(self, solution, i):
        g = self.problem.adj_matrix[i][i]

        for j, s in enumerate(solution):
            if j != i:
                g += 2 * self.problem.adj_matrix[j][i] * (1 if s else 0)

        g = g * (1 - 2 * (1 if solution[i] else 0))

        return g

    def get_gains(self, solution):
        gs = [ self.calculate_gain(solution, i) for i in range(len(solution))]
        return gs

    def local_search_1opt(self, solution):
        gs = self.get_gains(solution)
        return solution

    def objective(self, solution):
        sum = 0
        for i in range(len(solution)):
            for j in range(len(solution)):
                sum = sum + (1 if solution[i] else 0) * (1 if solution[j] else 0) * self.problem.adj_matrix[i][j]
        return sum

    def update_pheromone(self, ibs):

        bs = self.best_solution
        rbs = self.reset_best_solution

        q_bs = self.objective(bs) + 0.5
        q_ibs = self.objective(ibs) + 0.5
        q_rbs = self.objective(rbs) + 0.5

        q_sum = q_bs + q_ibs + q_rbs

        q_bs = q_bs / q_sum
        q_ibs = q_ibs / q_sum
        q_rbs = q_rbs / q_sum

        m = []

        for i, val in enumerate(bs):
            m.append((q_bs * (1 if bs[i] else 0)) + (q_ibs * (1 if ibs[i] else 0)) + (q_rbs * (1 if rbs[i] else 0)))

        for i, val in enumerate(self.pheromone):
            self.pheromone[i] = ((1 - self.rho) * self.pheromone[i]) + (self.rho * m[i])
            if self.pheromone[i] > 1:
                self.pheromone[i] = 1
            elif self.pheromone[i] < 0:
                self.pheromone[i] = 0

    def compute_cf(self):

        sum = 0
        for p in self.pheromone:
            sum += max(1-p, p)

        sum /= len(self.pheromone)
        cf = 2 * sum - 1

        return cf

    def reset(self):
        self.pheromone = [0.5] * len(self.pheromone)

    def get_sub_cnj_nodes(self, b):

        sum = 0
        for bs in self.best_solution:
            sum += 1 if bs == b else 0

        if sum == 0 or sum == len(self.best_solution):
            return None

        sub_cnj_nodes = []

        for i, val in enumerate(self.best_solution):
            if val == b:
                sub_cnj_nodes.append(self.problem.cnj_nodes[i])

        return sub_cnj_nodes

    def iteration(self):

        iteration_best_solution_value = 0
        iteration_best_solution = None

        for i_ant in range(self.num_ant):

            solution = [random.random() < p for p in self.pheromone]
            ant_solution = self.local_search_1opt(solution)
            ant_solution_value = self.objective(ant_solution)

            if ant_solution_value > iteration_best_solution_value or i_ant == 0:
                iteration_best_solution = list(ant_solution)
                iteration_best_solution_value = ant_solution_value

        if iteration_best_solution_value > self.reset_best_solution_value or self.reset_best_solution is None:
            self.reset_best_solution = list(iteration_best_solution)
            self.reset_best_solution_value = iteration_best_solution_value

        if iteration_best_solution_value > self.best_solution_value or self.best_solution is None:
            self.best_solution = list(iteration_best_solution)
            self.best_solution_value = iteration_best_solution_value

        self.update_pheromone(iteration_best_solution)

        cf = self.compute_cf()

        # print(cf)

        if cf > 0.999:
            # print("reset")
            self.reset()
            self.reset_best_solution = None
            self.reset_best_solution_value = 0


        pass





pass
