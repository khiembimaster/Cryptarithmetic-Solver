import re

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
    for letter, digit in assignment.items():
        sanitized_statement = sanitized_statement.replace(letter, str(digit))
    print(eval(sanitized_statement))
    
    constraints = [sanitized_statement]

    positions = [m.start() for m in re.finditer(r"[A-Z]", sanitized_statement)]
    
    

    # Print the constraint string
    print(constraints)

    