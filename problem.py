class Problem:
    total_edges = 0
    total_nodes = 0
    adj_matrix = [0][0]


class SubProblem:
    total_edges = 0
    total_nodes = 0
    adj_matrix = [0][0]
    cnj_nodes = []

    def __init__(self, sub_cnj_vertices):
        self.cnj_nodes = sub_cnj_vertices
        self.total_nodes = len(sub_cnj_vertices)

    def initialize_matrix(self, problem):

        self.adj_matrix = [None] * self.total_nodes

        for i in range(self.total_nodes):
            self.adj_matrix[i] = [0.0] * self.total_nodes

        sum = [0] * self.total_nodes

        for i in range(self.total_nodes):
            for j in range(self.total_nodes):
                self.adj_matrix[i][j] = problem.adj_matrix[self.cnj_nodes[i]][self.cnj_nodes[j]]
                sum[i] = sum[i] + self.adj_matrix[i][j]

        for i in range(self.total_nodes):
            self.adj_matrix[i][i] -= sum[i]


