# solver con tagli di Gomory interi per il Set Covering Problem

import cplex
import math


def solve_problem_multiple_interi(instanceProblem, iteration_manager):

    model = cplex.Cplex()
    num_variables = instanceProblem.columns

    # si aggiungono variabili binarie al modello
    for j in range(num_variables):
        model.variables.add(names=['x' + str(j)], lb=[0.0], ub=[1.0])

    # si aggiunge la funzione obiettivo al modello
    for j in range(num_variables):
        model.objective.set_linear([(j, float(instanceProblem.costs[j]))])

    model.objective.set_sense(model.objective.sense.minimize)

    # si aggiungono i vincoli
    # prima si aggiungono i vincoli che sono piani di taglio
    if instanceProblem.cut_constraint_counter != 0:
        for i in range(instanceProblem.cut_constraint_counter):
            constraint = cplex.SparsePair(ind=[j for j in range(num_variables)], val=instanceProblem.matrix[i])
            model.linear_constraints.add(lin_expr=[constraint], senses=['L'], rhs=[instanceProblem.b_vector[i]],
                                         names=['c' + str(i)])
    # dopo si aggiungono i vincoli originali del problema
    for i in range(instanceProblem.cut_constraint_counter, instanceProblem.rows):
        constraint = cplex.SparsePair(ind=[j for j in range(num_variables)], val=instanceProblem.matrix[i])
        model.linear_constraints.add(lin_expr=[constraint], senses=['G'], rhs=[instanceProblem.b_vector[i]],
                                     names=['c' + str(i)])

    model.write("./formulazione.lp")
    model.solve()
    model.solution.write("./soluzione.lp")

    opt_value = str(model.solution.get_objective_value())
    print("\nValore ottimo della funzione obiettivo: " + str(model.solution.get_objective_value()))
    instanceProblem.optimal_solution.append(float(opt_value))


    # creiamo le disequazioni per effettuare i cutting plane, se necessario

    # stabiliamo il numero massimo di tagli che si possono aggiungere ad ogni iterazione per arrivare ad un massimo
    # di 30 iterazioni senza oltrepassare le 1000 righe della matrice (causa versione free di cplex)
    num_max_cuts = math.floor((1000-instanceProblem.original_rows)/30)
    cuts_counter = 0

    # la posizione j occupata in basis_variables_indexes dalla variabile in base con valore ottimo
    # frazionario, corrisponde al numero di riga del tableau (e quindi all'indice del vincolo) da
    # considerare per il taglio. In optimal_values_basis_variables alla medesima posizione j si trova il
    # corrispondente valore ottimo del rilassamento lineare della variabile in base considerata
    optimal_values_basis_variables = model.solution.basis.get_header()[1]  # valori ottimi delle variabili in base
    basis_variables_indexes = model.solution.basis.get_header()[0]  # indici delle variabili in base
    create_cut_constraint = False
    # rappresenta la lista degli indici delle righe del tableau finale considerate per i tagli
    cut_constraint_index_list = []

    for j in range(len(basis_variables_indexes)):
        # se l'indice della variabile in base è >= 0 è una variabile strutturale, se l'indice è < 0 è una variabile di
        # slack o di surplus
        if basis_variables_indexes[j] >= 0:
            # con 0 selezioniamo la parte frazionaria
            double_part = math.modf(optimal_values_basis_variables[j])[0]
            # selezioniamo tutti i dizionario per il taglio corrispondenti alle variabili
            # frazionarie della soluzione ottima del rilassamento lineare
            if double_part != 0.0 and cuts_counter < num_max_cuts:
                create_cut_constraint = True
                cut_constraint_index_list.append(j)
                cuts_counter = cuts_counter + 1
            if (cuts_counter >= num_max_cuts):
                break


    if create_cut_constraint:

        # ora che sappiamo quanti sono i tagli, possiamo aggiungerli al modello
        instanceProblem.rows = instanceProblem.rows + len(cut_constraint_index_list)

        # si crea una matrice rows x columns tutta settata a 0
        new_matrix = [[0] * num_variables for i in range(instanceProblem.rows)]

        # si crea un nuovo vettore b tutto settato a 1
        new_b_vector = [1.0] * instanceProblem.rows

        for index in range(len(cut_constraint_index_list)):
            cut_constraint_coefficients = model.solution.advanced.binvarow(cut_constraint_index_list[index])
            for j in range(num_variables):
                int_part = math.floor(cut_constraint_coefficients[j])
                cut_constraint_coefficients[j] = int_part

            # si aggiunge alla matrice il nuovo vincolo di cutting plane
            new_matrix[index] = cut_constraint_coefficients

            # si aggiunge al vettore b dei termini noti il nuovo termine noto dato dalla parte intera del valore ottimo
            # della variabile del vincolo selezionato per il taglio
            new_b_vector[index] = math.floor(optimal_values_basis_variables[cut_constraint_index_list[index]])

        # si aggiungono alla matrice i vincoli iniziali
        j = 0
        for i in range(len(cut_constraint_index_list), instanceProblem.rows):
            new_matrix[len(cut_constraint_index_list) + j] = instanceProblem.matrix[j]
            j = j + 1

        # si aggiungono al vettore b i termini noti iniziali
        j = 0
        for i in range(len(cut_constraint_index_list), instanceProblem.rows):
            new_b_vector[len(cut_constraint_index_list) + j] = instanceProblem.b_vector[j]
            j = j + 1

        # si incrementa il contatore dei vincoli che sono piani di taglio
        instanceProblem.cut_constraint_counter = instanceProblem.cut_constraint_counter + len(cut_constraint_index_list)

        instanceProblem.matrix = new_matrix
        instanceProblem.b_vector = new_b_vector

        # controllo del numero di righe della matrice: se è pari a 1000 l'algoritmo si interrompe (causa versione
        # free cplex)
        if instanceProblem.rows >= 1000:
            return None

        # impostiamo i valori nell'itaration mangager e verifichiamo se ci sono le condizioni per contiuare le
        # iterazioni
        last_objective_function_value = model.solution.get_objective_value()
        previous_objective_function_value = iteration_manager.last_objective_function_value

        if previous_objective_function_value != 0:

            difference_percent = ((
                                          last_objective_function_value - previous_objective_function_value) /
                                  previous_objective_function_value) * 100

            if difference_percent >= iteration_manager.percent_limit:
                iteration_manager.last_objective_function_value = last_objective_function_value
                iteration_manager.is_difference_limit = False
                instanceProblem.num_try += 1
                solve_problem_multiple_interi(instanceProblem, iteration_manager)

            elif iteration_manager.is_difference_limit:
                return None
            else:
                iteration_manager.last_objective_function_value = last_objective_function_value
                iteration_manager.is_difference_limit = True
                instanceProblem.num_try += 1
                solve_problem_multiple_interi(instanceProblem, iteration_manager)

        else:
            iteration_manager.last_objective_function_value = last_objective_function_value
            solve_problem_multiple_interi(instanceProblem, iteration_manager)

    else:
        return None
