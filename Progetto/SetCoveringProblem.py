
class SetCoveringProblem:

    def __init__(self, original_rows, rows, columns, costs, matrix, b_vector, cut_constraint_counter, optimal_solution, num_try):
        self.original_rows = original_rows
        self.rows = rows
        self.columns = columns
        self.costs = costs
        self.matrix = matrix
        self.b_vector = b_vector
        self.cut_constraint_counter = cut_constraint_counter
        self.optimal_solution = optimal_solution
        self.num_try = num_try