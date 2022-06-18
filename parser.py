from enum import Enum, auto
from dataclasses import dataclass
import re
from typing import Optional, Tuple
from tokens import *


def split(string: str) -> Tuple[str, str]:
    fst = string.split()[0]
    rst = string[:len(fst)]
    return fst, rst


def parse(src):
    pass


def parse_instruction(src: str) -> Tuple[Instruction, str]:
    # remove any comments
    comment = re.search(r'\s*;.*', src)
    if comment is not None:
        src = src[:comment.start()]
    operation, src = parse_operation(src)


def parse_operation(src: str) -> Tuple[Operation, str]:
    dot = re.search(r'.', src)
    if dot is None:
        opcode = str_to_opcode(src)
    elif len(dot.groups()) == 2:
        pass
    else:
        raise Exception(f'Operation must be in format OPR or OPR.M. Got: {src.split("\n")[0]}')
    

def str_to_opcode(src: str) -> Opcode:
    match src:
        case 'dat':
            return Opcode.DAT
        case 'mov':
            return Opcode.MOV
        case 'add':
            return Opcode.MOV
        case 'sub':
            return Opcode.SUB
        case 'mul':
            return Opcode.MUL
        case 'div':
            return Opcode.DIV
        case 'mod':
            return Opcode.MOD
        case 'jmp':
            return Opcode.JMP
        case 'jmz':
            return Opcode.JMZ
        case 'jmn':
            return Opcode.JMN
        case 'djn':
            return Opcode.DJN
        case 'cmp':
            return Opcode.CMP
        case 'slt':
            return Opcode.SLT
        case 'spl':
            return Opcode.SPL
        case _:
            raise Exception(f'Unrecognized opcode: "{src}"')


def opcode_to_default_modifier(opcode: Opcode) -> OpcodeModifier:
    match opcode:
        case


def parse_opcode_modifier(src: str) -> Tuple[OpcodeModifier, str]:
    fst, rst = split(src)
    match fst:
        case 'a':
            return OpcodeModifier.A, rst
        case 'b':
            return OpcodeModifier.B, rst
        case 'ab':
            return OpcodeModifier.AB, rst
        case 'ba':
            return OpcodeModifier.BA, rst
        case 'f':
            return OpcodeModifier.F, rst
        case 'x':
            return OpcodeModifier.X, rst
        case 'i':
            return OpcodeModifier.I, rst
        case _:
            raise Exception(f'Unrecognized opcode modifier: "{fst}"')


def parse_addressing_mode(src: str) -> Optional[Tuple[AddressingMode, str]]:
    fst, rst = split(src)
    match fst:
        case '#':
            return AddressingMode.immediate, rst
        case '$':
            return AddressingMode.direct, rst
        case '@':
            return AddressingMode.indirect, rst
        case '<':
            return AddressingMode.predecrement_indirect, rst
        case '>':
            return AddressingMode.postincrement_indirect, rst
        case _:
            raise Exception(f'Unrecognized addressing mode: "{fst}"')
