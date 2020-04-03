
from SetCoveringProblem import SetCoveringProblem


def setting_data_problem(filename):

    file_txt = open(str(filename[0]))

    # si legge la prima riga che fornisce il numero di colonne e di righe della matrice
    line = file_txt.readline()
    matrix_dimensions = line.split()
    rows = int(matrix_dimensions[0])
    columns = int(matrix_dimensions[1])

    # si legge il vettore dei costi delle colonne
    costs_counter = 0
    costs = []
    while costs_counter != columns:
        line = file_txt.readline()
        split_array = line.split()

        for i in range(len(split_array)):
            costs.append(split_array[i])
            costs_counter = costs_counter + 1

    # si leggono i valori della matrice
    # si crea una matrice rows x columns tutta settata a 0
    matrix = [[0] * columns for i in range(rows)]

    # settiamo a 1 le colonne della matrice che leggiamo dal file
    for i in range(rows):
        line = file_txt.readline()
        split_array = line.split()
        num_columns_one = int(split_array[0])
        one_read = 0

        while one_read != num_columns_one:
            line = file_txt.readline()
            split_array = line.split()

            for j in range(len(split_array)):
                current_column = int(split_array[j]) - 1
                matrix[i][current_column] = 1
                one_read = one_read + 1

    # settiamo ad 1 il valore di tutti i termini noti dei vincoli
    b_vector = [1.0]*rows

    # impostiamo a 0 il contatore dei vincoli che sono piani di taglio
    cut_constraint_counter = 0
    num_try = 1
    optimal_solution = []

    instanceProblem = SetCoveringProblem(rows, rows, columns, costs, matrix, b_vector, cut_constraint_counter, optimal_solution, num_try)

    return instanceProblem
