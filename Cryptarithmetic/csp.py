class Constraint:
    def __init__(self, variables, constraint):
        self.variables = variables
        self.constraint = constraint
    def satisfied(self, assignment:dict = None):
        if not (set(self.variables) <= set(assignment.keys())):
            return True
        
        temp = self.constraint
        for letter, digit in assignment.items():
            temp = temp.replace(letter, str(digit))
        
        try:
            result = eval(temp) 
        except:
            result = False
        return result 

class CSP():
    def __init__(self, variables:set, domains:dict) -> None:
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
        print(assignment)
        if len(assignment) == len(self.variables):
            return assignment
        

        front = self.mrv(assignment)
        # unassigned = [var for var in self.variables if var not in assignment]
        # front = unassigned[0]
        
        for value in self.lcv(front, assignment):
            local_assignment = assignment.copy()
            local_assignment[front] = value
            if self.consistent(front, local_assignment) == 0:
                removals = self.suppose(front, value)
                if self.inference(removals=removals, assignment=local_assignment):
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
            return self.consistent(var, local)
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
    
    def get_neighbor(self, variable):
        neighbors = set()
        for contraint in self.constraints[variable]:
            neighbors.update(contraint.variables)
        neighbors.remove(variable)
        return neighbors
    
    def inference(self, queue=None, removals=None, assignment = None):
        if queue is None:
            queue = [(Xi, Xk) for Xi in self.variables for Xk in self.get_neighbor(Xi)]
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
        while queue:
            (Xi, Xj) = queue.pop()
            if self.revise(Xi, Xj, removals, assignment=assignment):
                if not self.curr_domains[Xi]:
                    return False
                for Xk in self.get_neighbor(Xi):
                    if Xk != Xi:
                        queue.append((Xk, Xi))
        return True

    def revise(self, Xi, Xj, removals, assignment:dict):
        revised = False
        for x in self.curr_domains[Xi][:]:
            conflict_list = []
            for y in self.curr_domains[Xj]:
                local = assignment.copy()
                local[Xi] = x
                local[Xj] = y
                if self.consistent(Xi, local) > 0:
                    conflict_list.append(True)
                else:
                    conflict_list.append(False)

            if all(conflict_list):
                self.prune(Xi, x, removals)
                revised = True
        
        return revised
        