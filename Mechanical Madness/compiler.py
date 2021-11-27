def get_instruction_type(instruction):
    if instruction[0] == ':':
        return 'label'
    return 'instruction'

def get_opcode(instr):
    translate_table = [
        "add",
        "sub",
        "mul",
        "clr",
        "rst",
        "jmp",
        "ljmp",
        "jlp",
        "jg",
        "jge",
        "jl",
        "jle",
        "je",
        "jz",
        "jnz",
        "mov",
        "movl",
        "call",
        "ret",
        "cmp",
        "push",
        "pop",
        "div",
        "mmiv",
        "mmov",
        "",
        "msk",
        "mskb"
    ]
    return format(translate_table.index(instr), '02x')


def get_label_encoded(word, labels):
    # Very ugly but there is only one so it's fine
    if '+1' in word:
        return '2f'
    else:
        return labels[word]

def get_operand_code(word, labels):
    regs = ['ax', 'bx', 'cx', 'dx']
    if ':' in word:
        return get_label_encoded(word, labels)
    if 'x' in word:
        if word in regs:
            return format(regs.index(word), '02x')
        else:
            return format(int(word, 16), '02x')
    else:
        return format(int(word), '02x')


def get_instruction_sequence(instruction, labels):
    words = instruction.split()
    opcode = get_opcode(words[0])
    op1 = '00'
    op2 = '00'
    if len(words) == 3:
        op1 = get_operand_code(words[1].strip(','), labels)
        op2 = get_operand_code(words[2], labels)
    return opcode + op1 + op2

if __name__ == '__main__':
    # don't forget to add the ':' in front of sub5 line 53 or compiler will crash
    program_file = './program.asm'
    output_file = './program.data'
    filestream = open(program_file)
    program = filestream.read().splitlines()
    filestream.close()
    labels = {}
    data = []
    for index, instruction in enumerate(program):
        type = get_instruction_type(instruction)
        if type == 'label':
            labels[instruction] = format(index - len(labels), '02x')
    # print(labels)
    for instruction in program:
        type = get_instruction_type(instruction)
        if type == 'instruction':
            data.append(get_instruction_sequence(instruction.strip(), labels))
    filestream = open(output_file, 'w')
    filestream.write(' '.join(data))
    filestream.close()
    print('Program has been compiled in :', output_file)
        

        

