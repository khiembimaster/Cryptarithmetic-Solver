solution = {'A': 7, 'H': 5, 'T': 9, 'S': 3, 'M': 2, 'O': 1, 'E': 0, 'R': 8, 'N': 6, 'Y': 4}
def evaluate(statement, assignment):
    temp = statement
    for letter, digit in assignment.items():
        temp = temp.replace(letter, str(digit))
    
    result = eval(temp) 
    return result

test = " ".join([
        "SO + MANY + MORE + MEN + SEEM + TO + SAY + THAT + THEY + MAY + SOON + TRY + TO + STAY + AT + HOME + ",
        "SO + AS + TO + SEE + OR + HEAR + THE + SAME + ONE + MAN + TRY + TO + MEET + THE + TEAM + ON + THE + ",
        "MOON + AS + HE + HAS + AT + THE + OTHER + TEN == TESTS"        
    ])
print(evaluate(test, solution))