import re
import time
import os
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

def evaluate(statement, assignment):
    temp = statement
    for letter, digit in assignment.items():
        temp = temp.replace(letter, str(digit))
    
    result = eval(temp) 
    return result

class Goal(Constraint):
    def __init__(self, variables, statement):
        super().__init__(variables)
        self.symbols = {}
        self.statement = statement
    def satisfied(self, assignment: dict = None):
        if not (set(self.variables) <= set(assignment.keys())):
            return True

        return evaluate(self.statement, assignment)
    
def remove_parentheses(s:str):
    # Find all pairs of parentheses that contain only addition or subtraction
    pattern = r'\(([+\-\w\s]+)\)'
    match = re.search(pattern, s)
    while match:
        # Distribute the terms inside the parentheses over the terms outside the parentheses
        inside = match.group(1).strip()
        start = match.start()
        if start > 0:
            if s[start-1] == '-':
                if str(s[start+1]).isalpha():
                    inside = '+' + inside[:]    
                s = s[:start-1] + s[start:]
                
                replacement =  inside.replace('+', 'temp').replace('-', '+').replace('temp', '-')
            else:
                replacement = inside
        else:
            replacement = inside
        # Replace the parentheses with the distributed terms
        s = s.replace(match.group(0), replacement)
        
        # Find the next pair of parentheses
        match = re.search(pattern, s)
    
    return s

def create_csp(statement):
    # Sanitize the input to remove invalid characters and operators
    sanitized_statement = re.sub(r'[^A-Za-z0-9+\-*\/\(\)\=]', '', statement)
    sanitized_statement = re.sub(r'\=', '==', sanitized_statement)
    sanitized_statement = remove_parentheses(sanitized_statement)
    # Use regular expressions to extract the variables and operands
    variables = set(re.findall(r'[A-Z]', sanitized_statement))
    Diffset = list(variables.copy())
    operands = re.findall(r'[A-Z]+', sanitized_statement)
    operators = re.findall(r'[\-\+]', sanitized_statement)
    print(sanitized_statement)
    print(variables)
    print(operands)

    if len(variables) > 10:
        return None

    non_zero_constraints = []
    #rang buoc khac 0
    for i in range(len(operands)):
        non_zero_constraints.append((operands[i][0]))

    # add constraints basic 
    numCarry= len(max(operands,key=len))
    
    for i in range(len(operands)):
        operands[i] = "{:0>{}}".format(operands[i], numCarry)
        operands[i] = operands[i][::-1]
    
    c = ''
    d = ''
    solution = None
    possibe_digits = {}
    Columns = []
    constraints = []
    sp_variables = set()
    d_array = ['0'for i in range(numCarry+1)] 
    for letter in variables:
        possibe_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    operators.insert(0,'+')
    for i in range(numCarry):
        # possibe_digits[f'd{i}{0}'] = [0,1,2,3,4,5,6,7,8,9]
        for j in range(len(operands)-1):
            d_array[i] += f'{operators[j]} {operands[j][i]}'
            
        temp = f'({d_array[i]})%10 == {operands[-1][i]}'
        used_variables = set(re.findall(r'[A-Z]', temp))
        constraints.append(Goal(used_variables, temp))
        d_array[i+1]=f'({d_array[i]})//10'
        
    csp = CSP(variables, possibe_digits)

    for constraint in non_zero_constraints:
        csp.regis_constraint(NonZero(constraint))

    for constraint in constraints:
        csp.regis_constraint(constraint)
    
    for i in range(len(Diffset)):
        for j in range(len(Diffset)):
            if i != j:
                csp.regis_constraint(Alldiff([Diffset[i], Diffset[j]]))
    csp.regis_constraint(Goal(Diffset, sanitized_statement))
    

    return csp    


def sort_solution_alphabetically(solution):
    sorted_solution = sorted(solution.items(), key=lambda x: x[0])
    return sorted_solution

def read_input_from_file(input_file_path):
    with open(input_file_path, 'r') as input_file:
        input_data = input_file.readlines()
    return input_data

def read_input_from_folder(main_folder_path):
    input_data_list = []
    i = input("Choose your level: ")  # Prompt for the level
    input_folder = os.path.join(main_folder_path, f'level_{i}')  
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)
            input_data = read_input_from_file(file_path)
            input_data_list.append((file_path, input_data))
    return input_data_list


def write_output_to_folder(input_file_path, output_data):
    output_subfolder = os.path.join(os.path.dirname(input_file_path), 'output')
    os.makedirs(output_subfolder, exist_ok=True)

    output_file_path = os.path.join(output_subfolder, f"output_{os.path.basename(input_file_path)}")
    with open(output_file_path, 'w') as output_file:
        for _, value in output_data:  
            output_file.write(f"{value}")

def solve_cryptarithmetic_puzzles(main_folder):
    # Read input from the input folder inside the main folder
    input_data_list = read_input_from_folder(main_folder)

    # Solve each Cryptarithmetic puzzle and store the solutions
    output_data_list = []
    for input_file_path, input_data in input_data_list:
        start = time.time()
        puzzle = ''.join(input_data).strip()
        csp = create_csp(puzzle)
        solution = csp.backtracking()
        sorted_solution = sort_solution_alphabetically(solution)
        end = time.time()
        write_output_to_folder(input_file_path, sorted_solution)
        elapsed_time = end - start
        print(f"Elapsed time: {elapsed_time} seconds")
        



if __name__ == "__main__":
    main_folder = 'main_folder'
    solve_cryptarithmetic_puzzles(main_folder)
    