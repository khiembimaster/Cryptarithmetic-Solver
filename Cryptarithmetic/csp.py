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
    def __init__(self, variables, domains:dict) -> None:
        self.variables = variables
        self.domains = domains 
        self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("This variable have no assigned domain.")

    def regis_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in self")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        count = 0
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                count+=1
        return count
    
    def suppose(self, variable, value):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

        removals = [(variable, a) for a in self.curr_domains[variable] if a != value]
        self.curr_domains[variable] = [value]
        return removals

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)    
    
    def prune(self, variable, value, removals):
        "Rule out variable=value."
        self.curr_domains[variable].remove(value)
        if removals is not None:
            removals.append((variable, value))

    def backtracking(self, assignment = {}):
        if len(assignment) == len(self.variables):
            return assignment
        

        front = self.mrv(assignment)
        # unassigned = [var for var in self.variables if var not in assignment]
        # front = unassigned[0]

        for value in self.domains[front]:
            local_assignment = assignment.copy()
            local_assignment[front] = value
            if self.consistent(front, local_assignment) == 0:
                removals = self.suppose(front, value)
                if self.inference(front, value, local_assignment, removals):
                    result = self.backtracking(local_assignment)
                    if result is not None:
                        return result
                self.restore(removals)
            
        return None
    def choices(self, var):
        "Return all values for var that aren't currently ruled out."
        return (self.curr_domains or self.domains)[var]
    
    def lcv(self, var, assignment):
        "Least-constraining-values heuristic."
        def plus_consistent(val):
            local = assignment.copy()
            local[var] = val
            self.consistent(var, local)
        return sorted(self.choices(var), key=plus_consistent)
    
    def mrv(self, assignment):
        "Minimum-remaining-values heuristic."
        return min([v for v in self.variables if v not in assignment], key=lambda var:self.num_legal_values(var, assignment))

    def num_legal_values(self, variable, assignment):
        sum = 0
        for value in self.domains[variable]:
            local_assignment = assignment.copy()
            local_assignment[variable] = value 
            sum += (self.consistent(variable, local_assignment) == 0 )
        return sum
    def inference(self, variable, value, assignment, removals):
        for B in self.variables:
            if B not in assignment:
                local = assignment.copy() 
                for b in self.curr_domains[B][:]:
                    local[B] = b
                    if self.consistent(variable, local) != 0:
                        self.prune(B, b, removals)
                if not self.curr_domains[B]:
                    return False
        return True
    
    