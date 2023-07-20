class Constraint:
    def __init__(self, variables, constraint):
        self.variables = variables
        self.constraint = constraint
    def satisfied(self, assignment:dict = None):
        if len(set(assignment.values())) < len(assignment):
            return False
         
        if len(assignment) != len(self.variables):
            return True

        temp = self.constraint
        for letter, digit in assignment.items():
            temp = temp.replace(letter, str(digit))
        return eval(temp)

class CSP():
    def __init__(self, variables, domains) -> None:
        self.variables = variables
        self.domains = domains 
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("This variable have no assigned domain.")

    def regis_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking(self, assignment = {}):
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [var for var in self.variables if var not in assignment]

        front = unassigned[0]
        
        for value in self.domains[front]:
            local_assignment = assignment.copy()
            local_assignment[front] = value
            if self.consistent(front, local_assignment):
                result = self.backtracking(local_assignment)

                if result is not None:
                    return result
        
        return None