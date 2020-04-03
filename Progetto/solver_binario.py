# solver per il Set Covering Problem nella programmazione lineare intera (variabili binarie)

import cplex


def solve_problem_binario(instanceProblem):
    model = cplex.Cplex()
    num_variables = instanceProblem.columns

    # si aggiungono variabili binarie al modello
    for j in range(num_variables):
        model.variables.add(names=['x' + str(j)], types=model.variables.type.binary)

    # si aggiunge la funzione obiettivo al modello
    for j in range(num_variables):
        model.objective.set_linear([(j, float(instanceProblem.costs[j]))])

    model.objective.set_sense(model.objective.sense.minimize)

    # si aggiungono i vincoli
    for i in range(instanceProblem.rows):
        constraint = cplex.SparsePair(ind=[j for j in range(num_variables)], val=instanceProblem.matrix[i])
        model.linear_constraints.add(lin_expr=[constraint], senses=['G'], rhs=[1], names=['c' + str(i)])

    model.solve()

    print(" ******  Valore ottimo della funzione obiettivo: " + str(model.solution.get_objective_value()) + "  ******** ")

    return str(model.solution.get_objective_value())

