from abc import ABC, abstractmethod


class CSP():

    def __init__(self, variables, domains, neighbors, contraints) -> None:
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = contraints

    def assign(self, variable, value, assignment):
        assignment[variable] = value

    def unassign(self, variable, assignment):
        if variable in assignment:
            del assignment[variable]

    def nconflicts(self, variable, value, assignment):
        def conflict(var):
            return (var in assignment and not self.constraints(variable, value, var, assignment[var]))
        return sum([1 for v in self.neighbors[variable] if conflict(v)])
    
    def suppose(self, variable, value):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variableiables}
        
        removals = [(variable, a) for a in self.curr_domains[variable] if a != value]
        self.curr_domains[variable] = [value]
        return removals

    def prune(self, variable, value, removals):
        self.curr_domains[variable].remove(value)
        if removals is not None:
            removals.append((variable, value))
    
    def choices(self, variable):
        return (self.curr_domains or self.domains)[variable]
    
    def infer_assignment(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variableiables}
        
        return {v: self.curr_domains[v][0] for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    def backtracking(self, assignment = {}):
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [var for var in self.variables if var not in assignment]

        front = unassigned[0]
        
        for value in self.order_domain_values(front, assignment):
            if 0 == self.nconflicts(front, value, assignment):
                self.assign(front, value, assignment)
                removals = self.suppose(front, value)
                if self.AC3([(X, front) for X in self.neighbors[front]], removals):
                    result = self.backtracking(assignment)
                    if result is not None:
                        return result

                self.restore(removals)
        self.unassign(front, assignment)
        return None

    def order_domain_values(self, variable, assignment):
        if self.current_domains:
            domain = self.current_domains[variable]
        else:
            domain = self.domains[variable][:]

        while domain:
            yield domain.pop()
    

    def AC3(self, queue=None, removals = None):
        """[Fig. 5.7]"""
        if queue is None:
            queue = [(Xi, Xk) for Xi in self.variables for Xk in self.neighbors[Xi]]
        
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variableiables}
        
        while queue:
            (Xi, Xj) = queue.pop()
            if self.revise(Xi, Xj, removals):
                if not self.curr_domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xi:
                        queue.append((Xk, Xi))
        return True
    
    def revise(self, Xi, Xj, removals):
        revised = False
        for x in self.current_domains[Xi][:]:
            if all(not self.constraints(Xi, x, Xj, y) for y in self.curr_domains[Xj]):
                self.prune(Xi, x, removals)
                revised = True
        
        return revised

    # def mrv(self, assignment):
    #     return argmin_random_tie(
    #         [v for v in csp.variables if v not in assignment],
    #         key=lambda var: num_legal_values(csp, var, assignment))

    def lcv(self, variable, assignment):
        return sorted(self.choices(variable),
                  key=lambda val: self.nconflicts(variable, val, assignment))
