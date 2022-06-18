from lib2to3.pgen2.token import OP
from pickletools import OpcodeInfo
import re
from typing import Dict, List, Tuple

from tokens import Address, AddressingMode, Instruction, Opcode, LabelAddress, OpcodeModifier, Operation

STR_TO_OPCODE = {
    'dat': Opcode.DAT,
    'mov': Opcode.MOV,
    'add': Opcode.ADD,
    'sub': Opcode.SUB,
    'mul': Opcode.MUL,
    'div': Opcode.DIV,
    'mod': Opcode.MOD,
    'jmp': Opcode.JMP,
    'jmz': Opcode.JMZ,
    'jmn': Opcode.JMN,
    'djn': Opcode.DJN,
    'cmp': Opcode.CMP,
    'slt': Opcode.SLT,
    'spl': Opcode.SPL
}
STR_TO_MODE = {
    '#': AddressingMode.immediate,
    '$': AddressingMode.direct,
    '@': AddressingMode.indirect,
    '<': AddressingMode.predecrement_indirect,
    '>': AddressingMode.postincrement_indirect
}
STR_TO_MODIFIER = {
    'a': OpcodeModifier.a,
    'b': OpcodeModifier.b,
    'ab': OpcodeModifier.ab,
    'ba': OpcodeModifier.ba,
    'f': OpcodeModifier.f,
    'x': OpcodeModifier.x,
    'i': OpcodeModifier.i
}
def get_default_operator(opcode: Opcode,
                         a_mode: AddressingMode,
                         b_mode: AddressingMode) -> OpcodeModifier:
    # TODO: see table at the end of the spec

# remove all comments and blank lines
def preprocess_src(src: str) -> List[str]:
    src_lines = src.split('\n')
    for i, line in enumerate(src_lines):
        comment_match = re.search(r'\s*;.*', line)
        if comment_match is not None:
            src_lines[i] = line[:comment_match.start()]
    src_lines = filter(lambda line: re.search(r'\S', line) is not None, src_lines)
    return list(src_lines)

# scan through and create a label to line dict
def separate_labels_from_code(src: str) -> Tuple[List[str], str]:
    """
    Find all the labels before the opcode and return them in a list.
    Return the source code with those labels and extra whitespace removed.
    """
    words = src.split()
    labels = []
    rest = []
    found_instruction = False
    for word in words:
        is_instruction = word in STR_TO_OPCODE
        found_instruction = found_instruction or is_instruction
        if found_instruction:
            rest.append(word)
        if not is_instruction and word.isalpha():
            labels.append(word)
    return labels, ' '.join(rest)


def make_label_to_instno(src: List[str]) -> Tuple[Dict[str, int], List[str]]:
    """
    Return a dictionary of label to instruction number
    """
    label_to_instno = {}
    new_src = []
    for instno, line in enumerate(src):
        labels, new_src_line = separate_labels_from_code(line)
        if len(labels) == 0:
            continue
        for label in labels:
            label_to_instno[label] = instno
        new_src.append(new_src_line)
    return label_to_instno, new_src


# make a list of Instructions in the order that they appear in the file
def parse_instructions(src: List[str]) -> List[Instruction]:
    def parse_address(s: str) -> Tuple[Address | LabelAddress, str]:
        # TODO: add support for expressions
        if s[0].isdigit():
            mode = AddressingMode.direct
            start = 0
        elif s[0] in STR_TO_MODE:
            mode = STR_TO_MODE[s[0]]
            start = 1
        else:
            raise Exception(f'{s.split()[0]} does not contain a valid address')
        end = start
        while not s[end].isspace():
            if not s[end].isalnum():
                raise Exception(f'Expected integer or string, got {s[start:end]}')
            end += 1
        addr = s[start:end]
        if addr.isdecimal():
            return Address(int(addr), mode), s[end:]
        return LabelAddress(addr, mode), s[end:]

    def parse_instruction(line: str) -> Tuple[Opcode | Address | LabelAddress, str]:
        """
        Parses opcodes and pseudo-instructions (just org so far)
        """
        opcode_str = line.split()[0]
        if '.' in opcode_str:
            fields = opcode_str.split('.')
            opcode_str = fields[0]
            if opcode_str not in STR_TO_OPCODE:
                raise Exception(f'{opcode_str} not a valid opcode')
            opcode = STR_TO_OPCODE[opcode_str]
            modifier_str = fields[1]
            if modifier_str not in STR_TO_MODIFIER:
                raise Exception(f'{modifier_str} not a valid opcode modifier')
            modifier = STR_TO_MODIFIER[modifier_str]
            operation = Operation(opcode, modifier)
        else:
            if opcode_str not in STR_TO_OPCODE:
                raise Exception(f'{opcode_str} not a valid opcode')
            opcode = STR_TO_OPCODE[opcode_str]
            modifier = OPCODE_TO_DEF_MODIFIER[opcode]

        if opcode_str not in STR_TO_OPCODE:
            raise Exception(f'Expected opcode. Got {opcode_str}')
        opcode = STR_TO_OPCODE[opcode_str]

        # find the start of the next token (the address)
        start = len(opcode_str) + 1
        while line[start].isspace():
            start += 1
        # We were given the starting location of the program
        if opcode_str == 'org':
            address, rest = parse_address(line[start])
            return address, rest
        # This is just a normal instruction and therefore has an A and B field
        A, rest = parse_address(line[start])
        start = 0
        while rest[start].isspace():
            start += 1
        B, rest = parse_address(rest[start])
            
        

    instructions = []
    for line in src:
        opcode_str = find_opcode(line)
        # TODO: pull out addresses. remember that they can be labels or numbers
# replace the labels in the instruction list with the correct numbers