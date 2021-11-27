import re

def q(char):
    '''
    A modification of the original function q
    that convert array to string
    '''
    return chr((char * 59 - 54) & 255)

macro = open('macro', 'r')
for line in macro.readlines():
    chars = re.findall('([0-9]{1,})', line) # Get all int of Array
    if chars == []:
        continue
    for char in chars:
        char = q(int(char))
        print(char, end='')
    print()