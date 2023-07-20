import re
from csp import Constraint, CSP

class UnaryConstraint(Constraint):
    def __init__(self, variables, constraint):
        self.variables = variables
        self.constraint = constraint
    def satisfied(self, assignment:dict = None):
        temp = self.constraint
        for letter, digit in assignment.items():
            temp = temp.replace(letter, str(digit))
        return eval(temp)

if __name__ == "__main__":
    statement = "SEND+MORE=MONEY"
    # Sanitize the input to remove invalid characters and operators
    sanitized_statement = re.sub(r'[^A-Za-z0-9+\-*\/\(\)\=]', '', statement)
    sanitized_statement = re.sub(r'\=', '==', sanitized_statement)
    # Use regular expressions to extract the variables and operands
    variables = set(re.findall(r'[A-Z]', sanitized_statement))
    operands = re.findall(r'[A-Z]+', sanitized_statement)
    print(sanitized_statement)
    print(variables)
    print(operands)
    assignment = {'S': 9, 'E': 5, 'N': 6, 'D': 7, 'M': 1, 'O': 0, 'R': 8, 'Y': 2}

    possibe_digits = {}
    for letter in variables:
        possibe_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    csp = CSP(variables, possibe_digits)
    Cryptarithmetic = Constraint(variables, sanitized_statement)
    NoLeadingZero = [UnaryConstraint(['S'], 'S!=0')]
    NoLeadingZero.append(UnaryConstraint(['M'], 'M!=0'))
    csp.regis_constraint(NoLeadingZero[0])
    csp.regis_constraint(NoLeadingZero[1])
    csp.regis_constraint(Cryptarithmetic)

    solution = csp.backtracking()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)

    # constraints = [sanitized_statement]

    # positions = [m.start() for m in re.finditer(r"[A-Z]", sanitized_statement)]

    # constraint = '
    # # Print the constraint string
    # constraints.append(constraint)
    # print(eval(constraint))

    