import re
import time
from csp import Constraint, CSP

class Alldiff(Constraint):
    def __init__(self, variables):
        super().__init__(variables)
    def satisfied(self, assignment: dict = None):
        if not (set(self.variables) <= set(assignment.keys())):
            return True
        return assignment[self.variables[0]] != assignment[self.variables[1]]

class NonZero(Constraint):
    def __init__(self, variables):
        super().__init__(variables)
    def satisfied(self, assignment: dict = None):
        if not (set(self.variables) <= set(assignment.keys())):
            return True
        return assignment[self.variables] != 0

class Goal(Constraint):
    def __init__(self, variables, statement):
        super().__init__(variables)
        self.symbols = {}
        self.statement = statement
    def satisfied(self, assignment: dict = None):
        if not (set(self.variables) <= set(assignment.keys())):
            return True

        temp = self.statement
        for letter, digit in assignment.items():
            temp = temp.replace(letter, str(digit))
        try: 
            result = eval(temp) 
        except:
            return False
        return result
    
def create_csp(statement):
    # Sanitize the input to remove invalid characters and operators
    sanitized_statement = re.sub(r'[^A-Za-z0-9+\-*\/\(\)\=]', '', statement)
    sanitized_statement = re.sub(r'\=', '==', sanitized_statement)
    # Use regular expressions to extract the variables and operands
    variables = list(set(re.findall(r'[A-Z]', sanitized_statement)))
    operands = re.findall(r'[A-Z]+', sanitized_statement)
    print(sanitized_statement)
    print(variables)
    print(operands)
    if len(variables) > 10:
        return None
    
    Cryptarithmetic = Goal(variables.copy(), sanitized_statement)
    non_zero_constraints = []
    #rang buoc khac 0
    for i in range(len(operands)):
        non_zero_constraints.append((operands[i][0]))
    constraints = []
    for variable in set(non_zero_constraints):
        constraints.append(NonZero(variable))

    #AllDiff
    for i in range(len(variables)):
        for j in range(len(variables)):
            if i != j:
                constraints.append(Alldiff([variables[i], variables[j]]))

    possibe_digits = {}
    for letter in variables:
        possibe_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Register the constraints
    csp = CSP(variables, possibe_digits)
        
    for constraint in constraints:
        csp.regis_constraint(constraint) 
    csp.regis_constraint(Cryptarithmetic)
    return csp


if __name__ == "__main__":
    challenges = [
    
    " ".join(["SEND+MORE=MONEY",
    ]),
    " ".join(["SEND+(MORE+MONEY)-OR+DIE=NUOYI"
    ]),
    " ".join([
        "TEN + HERONS + REST + NEAR + NORTH + SEA + SHORE + AS + TAN + TERNS + SOAR + TO + ENTER + THERE + AS + ",
        "HERONS + NEST + ON + STONES + AT + SHORE + THREE + STARS + ARE + SEEN + TERN + SNORES + ARE + NEAR = SEVVOTH",        
    ]),
    " ".join([
        "SO + MANY + MORE + MEN + SEEM + TO + SAY + THAT + THEY + MAY + SOON + TRY + TO + STAY + AT + HOME + ",
        "SO + AS + TO + SEE + OR + HEAR + THE + SAME + ONE + MAN + TRY + TO + MEET + THE + TEAM + ON + THE + ",
        "MOON + AS + HE + HAS + AT + THE + OTHER + TEN = TESTS",
    ]),
]
    statement = "SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+MOON+AS+HE+HAS+AT+THE+OTHER+TEN=TESTS"

    csp = create_csp(challenges[3])

    start = time.time()

    # Code to be measured
    solution = csp.backtracking()
    solution = dict(sorted(solution.items()))
    end = time.time()
    elapsed_time = end - start
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
    print(f"Elapsed time: {elapsed_time} seconds")
    