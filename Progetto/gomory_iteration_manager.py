class GomoryIterationManager:

    def __init__(self, last_objective_function_value, is_difference_limit, percent_limit):
        self.last_objective_function_value = last_objective_function_value
        self.is_difference_limit = is_difference_limit
        self.percent_limit = percent_limit
