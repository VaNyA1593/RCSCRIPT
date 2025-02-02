from time import sleep

filename = input()

with open(filename, 'r') as file:
    lines = [line.strip() for line in file]

labels = {}
token_counter = 0
program = []
goto_manager = {}

for line in lines:
    token = line.split(" ")
    opcode = token[0]

    if opcode == '':
        continue

    token_counter += 1
    program.append(opcode)

    if opcode == 'retract':
        row = int(token[1])
        column = int(token[2])
        program.append(row)
        program.append(column)
        token_counter += 2

    elif opcode == 'retractcontract':
        row = int(token[1])
        column = int(token[2])
        program.append(row)
        program.append(column)
        token_counter += 2

    elif opcode == 'contract':
        row = int(token[1])
        column = int(token[2])
        program.append(row)
        program.append(column)
        token_counter += 2

    elif opcode == 'ruler':
        row = int(token[1])
        column = int(token[2])
        program.append(row)
        program.append(column)
        token_counter += 2

    elif opcode == 'foff':
        time = int(token[1])
        program.append(time)
        token_counter += 1

    elif opcode == 'loop':
        loop_name = token[4]
        number = int(token[2])
        program.append(number)
        program.append(loop_name)
        token_counter += 2
        goto_manager[loop_name] = token_counter

    elif opcode == 'rcloop':
        row = int(token[2])
        column = int(token[3])
        loop_name = token[5]
        retractcontractnum = f"{row},{column}"
        program.append(retractcontractnum)
        program.append(loop_name)
        token_counter += 2

        if loop_name not in goto_manager:
            goto_manager[loop_name] = token_counter

    elif opcode == 'endloop':
        program.append(token[1])
        token_counter += 1

    elif opcode == 'read':
        row = int(token[1])
        column = int(token[2])
        program.append(row)
        program.append(column)
        token_counter += 2

    elif opcode == 'label':
        label_name = token[1]
        program.append(label_name)
        labels[label_name] = token_counter
        token_counter += 1

    elif opcode == 'goto':
        label_name = token[1]
        program.append(label_name)
        token_counter += 1

    elif opcode == 'gotoifeq':
        row = int(token[1])
        column = int(token[2])
        number = int(token[3])
        label_name = token[4]
        program.append(row)
        program.append(column)
        program.append(number)
        program.append(label_name)
        token_counter += 4

    elif opcode == 'print':
        string = ' '.join(token[1:])
        program.append(string)
        token_counter += 1

    elif opcode == 'add':
        row1 = int(token[1])
        column1 = int(token[2])
        row2 = int(token[3])
        column2 = int(token[4])
        row3 = int(token[5])
        column3 = int(token[6])

        program.append(row1)
        program.append(column1)
        program.append(row2)
        program.append(column2)
        program.append(row3)
        program.append(column3)

        token_counter += 6

    elif opcode == 'sub':
        row1 = int(token[1])
        column1 = int(token[2])
        row2 = int(token[3])
        column2 = int(token[4])
        row3 = int(token[5])
        column3 = int(token[6])

        program.append(row1)
        program.append(column1)
        program.append(row2)
        program.append(column2)
        program.append(row3)
        program.append(column3)

        token_counter += 6

    elif opcode == 'retractcontracttable':
        rows = token[1]
        columns = token[2]
        number = int(token[3])
        program.append(rows)
        program.append(columns)
        program.append(number)
        token_counter += 3

table = {}

def retractcontract(row, column):
    table[f'{row},{column}'] = 0

def retract(row, column):
    table[f'{row},{column}'] += 1

def contract(row, column):
    table[f'{row},{column}'] -= 1

def ruler(row, column):
    return table.get(f'{row},{column}')

def read(row, column):
    number = input()
    table[f'{row},{column}'] = int(number)

def add(row1, column1, row2, column2, row3, column3):
    table[f'{row3},{column3}'] = table[f'{row1},{column1}'] + table[f'{row2},{column2}']

def subtract(row1, column1, row2, column2, row3, column3):
    table[f'{row3},{column3}'] = table[f'{row1},{column1}'] - table[f'{row2},{column2}']

def retractcontracttable(rows, columns, number):
    for row in range(int(rows)):
        for column in range(int(columns)):
            table[f'{row},{column}'] = number

def print_table():
    if not table:
        print("Table is empty.")
        return
    
    row_indices = set()
    col_indices = set()

    for key in table.keys():
        row, col = map(int, key.split(","))
        row_indices.add(row)
        col_indices.add(col)

    max_row = max(row_indices, default=0)
    max_col = max(col_indices, default=0)

    for row in range(max_row + 1):
        row_values = []
        for col in range(max_col + 1):
            value = table.get(f"{row},{col}", 0)
            row_values.append(str(value))
        print(" ".join(row_values))

pc = 0
loops = {}

while pc < len(program):  # Prevent out of range access
    opcode = program[pc]
    pc += 1

    if opcode == 'retract':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        retract(row, column)

    elif opcode == 'retractcontract':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        retractcontract(row, column)

    elif opcode == 'contract':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        contract(row, column)

    elif opcode == 'ruler':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        print(ruler(row, column))

    elif opcode == 'foff':
        time = program[pc]
        pc += 1
        sleep(time)

    elif opcode == 'loop':
        number = program[pc]
        pc += 1
        loop_name = program[pc]
        pc += 1
        loops[loop_name] = number

    elif opcode == 'rcloop':
        number = table[program[pc]]
        pc += 1
        loop_name = program[pc]
        pc += 1
        loops[loop_name] = number

    elif opcode == 'endloop':
        loop_name = program[pc]
        pc += 1

        if loops[loop_name] > 1:
            pc = goto_manager[loop_name]
            loops[loop_name] -= 1

    elif opcode == 'read':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        read(row, column)

    elif opcode == 'label':
        label_name = program[pc]
        pc += 1

    elif opcode == 'goto':
        label_name = program[pc]
        pc = labels[label_name]

    elif opcode == 'gotoifeq':
        row = program[pc]
        pc += 1
        column = program[pc]
        pc += 1
        number = program[pc]
        pc += 1
        label_name = program[pc]
        pc += 1

        value = ruler(row, column) or 0  

        if value == number:
            if label_name in labels:
                pc = labels[label_name]
            else:
                print(f"Error: Label '{label_name}' not found.")
                break

    elif opcode == 'print':
        string = program[pc]
        pc += 1
        print(string)

    elif opcode == 'add':
        row1 = program[pc]
        pc += 1
        column1 = program[pc]
        pc += 1
        row2 = program[pc]
        pc += 1
        column2 = program[pc]
        pc += 1
        row3 = program[pc]
        pc += 1
        column3 = program[pc]
        pc += 1
        add(row1, column1, row2, column2, row3, column3)

    elif opcode == 'sub':
        row1 = program[pc]
        pc += 1
        column1 = program[pc]
        pc += 1
        row2 = program[pc]
        pc += 1
        column2 = program[pc]
        pc += 1
        row3 = program[pc]
        pc += 1
        column3 = program[pc]
        pc += 1
        subtract(row1, column1, row2, column2, row3, column3)

    elif opcode == 'printmemory':
        print_table()

    elif opcode == 'retractcontracttable':
        rows = program[pc]
        pc += 1
        columns = program[pc]
        pc += 1
        number = program[pc]
        pc += 1
        retractcontracttable(rows, columns, number)

    elif opcode == 'end':
        break  # End program execution
