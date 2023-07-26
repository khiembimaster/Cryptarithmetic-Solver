solution = {'N': 7, 'S': 1, 'H': 3, 'R': 6, 'T': 9, 'A': 2, 'O': 4, 'E': 5, 'V': 8}
def evaluate(statement, assignment):
    temp = statement
    for letter, digit in assignment.items():
        temp = temp.replace(letter, str(digit))
    
    result = eval(temp) 
    return result

test = " ".join([
        "TEN + HERONS + REST + NEAR + NORTH + SEA + SHORE + AS + TAN + TERNS + SOAR + TO + ENTER + THERE + AS + ",
        "HERONS + NEST + ON + STONES + AT + SHORE + THREE + STARS + ARE + SEEN + TERN + SNORES + ARE + NEAR == SEVVOTH",        
    ])
print(evaluate(test, solution))