import re
import time
from csp import Constraint, CSP

def checkIndexNotCorrect(indexOperand:list):
    for i in range(len(indexOperand)-1):
        if(indexOperand[i]!=-1):
            return False
    return True


def create_csp(statement):
    # Sanitize the input to remove invalid characters and operators
    sanitized_statement = re.sub(r'[^A-Za-z0-9+\-*\/\(\)\=]', '', statement)
    sanitized_statement = re.sub(r'\=', '==', sanitized_statement)
    # Use regular expressions to extract the variables and operands
    variables = set(re.findall(r'[A-Z]', sanitized_statement))
    operands = re.findall(r'[A-Z]+', sanitized_statement)
    print(sanitized_statement)
    print(variables)
    print(operands)
    if len(variables) > 10:
        return None
    
    Cryptarithmetic = Constraint(variables.copy(), sanitized_statement)
    non_zero_constraints = []
    #rang buoc khac 0
    for i in range(len(operands)):
        temp=""
        temp+=operands[i][0]+"!=0"
        non_zero_constraints.append((operands[i][0], temp))
    constraints = []
    for variable, constraint in set(non_zero_constraints):
        constraints.append(Constraint(variable, constraint))

    #AllDiff
    AllDiff = list(variables.copy())
    for i in range(len(AllDiff)-1):
        for j in range(i+1, len(AllDiff)):
            temp = ''
            temp += AllDiff[i] + "!=" + AllDiff[j]
            constraints.append(Constraint([AllDiff[i], AllDiff[j]], temp))

    # add constraints basic 
    numCarry= len(max(operands,key=len))
    carry=[]
    for i in range(numCarry):
        temp='c'+str(i)
        carry.append(temp)
    indexOperands=[]
    for i in range(len(operands)):
        indexOperands.append(len(operands[i])-1)

    used_cary = set()
    for i in range(numCarry):
        used_variable = set()
        temp=""
        for ii in range(len(operands)-1):
            if indexOperands[ii]!=-1:
                temp+=operands[ii][indexOperands[ii]]
                used_variable.add(operands[ii][indexOperands[ii]])
                indexOperands[ii]-=1
                temp+='+'

        if i==0:
            temp=temp[:-1]
            temp+='=='
        else :
            temp+=carry[i-1]
            used_variable.add(carry[i-1])
            used_cary.add(carry[i-1])
            temp+='=='
        if (checkIndexNotCorrect(indexOperands) and i==numCarry-1):
            temp+=operands[ii+1][indexOperands[ii+1]]
            used_variable.add(operands[ii+1][indexOperands[ii+1]])
        else:
            temp+=operands[ii+1][indexOperands[ii+1]]+"+10*"+carry[i]
            used_variable.add(operands[ii+1][indexOperands[ii+1]])
            used_variable.add(carry[i])
            used_cary.add(carry[i])
            indexOperands[ii+1]-=1
        constraints.append(Constraint(used_variable, temp))

    variables.update(used_cary)


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

    csp = create_csp(challenges[0])

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
    