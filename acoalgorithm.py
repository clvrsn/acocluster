from ant_system import *
from problem import *
import time


def load_graph(filename):

    problem = Problem()

    y = []
    f = open(filename, 'r')

    lines_all = f.readlines()
    problem.total_nodes = int(lines_all[0])

    lines = [[int(n) for n in x.split()] for x in lines_all[1:]]

    problem.adj_matrix = [None] * problem.total_nodes

    for i in range(problem.total_nodes):
        problem.adj_matrix[i] = [0.0] * problem.total_nodes

    grau_verticies = [0.0] * problem.total_nodes

    for line in lines:
        problem.total_edges += 1
        problem.adj_matrix[line[0]-1][line[1]-1] = 1.0
        problem.adj_matrix[line[1]-1][line[0]-1] = 1.0
        grau_verticies[line[0]-1] += 1
        grau_verticies[line[1]-1] += 1

    for i in range(len(problem.adj_matrix)):
        for j in range(len(problem.adj_matrix[i])):
            # b_{ij} = Contribuição para a modularidade
            problem.adj_matrix[i][j] = problem.adj_matrix[i][j] - (
                grau_verticies[i] * grau_verticies[j] / (2 * problem.total_edges) )

    return problem


def get_communities():
    communities = []


def main(input_pathfile, output_pathfile):

    print("Executando "+ input_pathfile + " ... ")

    ini = time.time()
    modularity = 0
    comunities = []

    problem = load_graph(input_pathfile)

    cnj_nodes = []
    for i in range(problem.total_nodes):
        cnj_nodes.append(i)

    sub_problems = []
    sub_problem = SubProblem(cnj_nodes)
    sub_problems.append(sub_problem)

    while len(sub_problems) > 0:

        sub_problem = sub_problems.pop(0)
        sub_problem.initialize_matrix(problem)

        ant = AntSystem(sub_problem)

        for i in range(100):
            ant.iteration()

        if ant.best_solution_value > (0.01 * problem.total_edges):
            modularity += ant.best_solution_value / problem.total_edges
            cnj_nodes_tmp = ant.get_sub_cnj_nodes(True)
            sub_problem = SubProblem(cnj_nodes_tmp)
            sub_problems.append(sub_problem)
            cnj_nodes_tmp = ant.get_sub_cnj_nodes(False)
            sub_problem = SubProblem(cnj_nodes_tmp)
            sub_problems.append(sub_problem)
            pass
        else:
            comunities.append(sub_problem.cnj_nodes)
    pass

    fim = time.time()

    fout = open(output_pathfile, 'w')
    fout.write("Modularidade: %f\n" % modularity)
    fout.write("Tempo execução: %f\n" % (fim - ini))
    fout.write("Número de Comunidades: %d\n" % len(comunities))
    fout.write("Comunidades:\n")

    ic = 0
    for c in comunities:
        for n in c:
            fout.write("%d %d\n" % (ic, n))
        ic += 1


if __name__ == "__main__":
    main("input_simple.txt", "output_simple.txt")
    main("input_karate.txt", "output_karate.txt")
    main("input_metabolic.txt", "output_metabolic.txt")
    main("input_jazz.txt", "output_jazz.txt")
    main("input_email.txt", "output_email.txt")
