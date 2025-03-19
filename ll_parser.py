# this opens and reads the file
def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found.")

# this separates the alphanumeric identifiers to special characters
def tokenize(text):
    tokens = [] # holds all the tokens
    token = '' # holds alphanumeric identifiers
    quotation = '' # holds strings within quotation marks
    inQuotation = 0 # indicator for quotation marks

    for char in text:   
        # check if the character is a quotation mark
        if char == '"' or char == "'":
            inQuotation += 1
            continue

        # 1 indicates the loop is inside a quotation mark
        if inQuotation == 1:
            quotation += char
            continue

        # 2 indicates the closing quotation mark
        if inQuotation == 2:
            tokens.append(quotation) # adds the whole quotation to list of tokens
            quotation = ''
            inQuotation = 0

        # add the alphanumeric identifier to the token
        if char.isalnum():
            token += char
            continue
        
        # this prevents from adding white spaces as tokens
        if token != '':
            tokens.append(token)
            token = ''

        # checks if the character is a special character
        if char in " \n":
            continue

        # adds the special character to the list of tokens
        tokens.append(char)
    return tokens

# this gets the rules and terminals from the file
def get_rules(text):
    rules = {} # holds all the rules
    terminals = {}
    grammar = text.split("\n")

    for rule in grammar:
        temp = rule.split(" -> ")

        # left hand side
        lhs = temp[0]

        # right hand side
        rhs  = temp[1].split(" | ")
        clean_rhs = [] 
        for i in rhs:
            clean = ''
            for j in i.split():
                clean += j
            clean_rhs.append(clean)
        rules.update({lhs:clean_rhs})

        # get terminals
        lhs_terminals = []
        for i in rhs:
            nonterminal_count = 0

            for j in i:
                if j.isupper():
                    nonterminal_count += 1
            
            if nonterminal_count == 0:
                lhs_terminals.append(i)
        
        if len(lhs_terminals) > 0:
            terminals.update({lhs:lhs_terminals})

    return rules, terminals

# this brute forces the creation of all possible combinations
def parsing(string, rules, terminals):
    all_lhs = rules.keys()
    derivatives = []
    target_string = ''

    # convert the list of tokens to a string
    for c in string:
        target_string += c

    # create all possible combinations
    start_rule = list(rules.keys())[0]
    for i in rules[start_rule]:
        path = []
        path.append(i)
        get_combinations(target_string, rules, i, path, derivatives, terminals)

# this gets all the possible combinations using the rules
def get_combinations(target_string, rules, current_combination, path, derivatives, terminals):
    for i in range(len(current_combination)):
        if current_combination[i].isupper():
            current_rules = rules[current_combination[i]]

            for j in current_rules:
                # replace the nonterminal
                new_combination = current_combination[:i] + j + current_combination[i+1:]
                
                current_path = path.copy()
                current_path.append(new_combination)

                # check if the new combination is equal to the target string
                if len(new_combination) == len(target_string):
                    derivatives.append((new_combination, current_path))           
                    convert_derivatives(new_combination, current_path, terminals, target_string)
                
                # else create a new combination
                else:
                    get_combinations(target_string, rules, new_combination, current_path, derivatives, terminals)  

# this converts the nonterminals to terminals
def convert_derivatives(derivative, current_path, terminals, target_string):
    for j in range(len(derivative)):
        # check if the character is nonterminal
        if derivative[j].isupper():
            j_terminals = terminals.get(derivative[j])

            if j_terminals is None:
                continue
            
            # create a new combination with the terminals
            for k in j_terminals:
                derivative = derivative[:j] + k + derivative[j+1:]
                current_path.append(derivative)
    
    # check if the new combination is equal to the target string
    if derivative == target_string:
        print(f'Target String:\t{target_string} \nDerivation:', end='\t')
        for i in range(len(current_path)):
            if i == len(current_path) - 1:
                print(current_path[i])
            else:
                print(current_path[i], end=' -> ')
        print()

# main function 
def main():
    string = read_file('string.txt')
    tokens1 = tokenize(string)

    production_rules = read_file('production_rules.txt')
    tokens2, terminals = get_rules(production_rules)

    parsing(tokens1, tokens2, terminals)

main()