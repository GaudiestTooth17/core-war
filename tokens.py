from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class OpcodeModifier(Enum):
    a = auto()
    b = auto()
    ab = auto()
    ba = auto()
    f = auto()
    x = auto()
    i = auto()


class AddressingMode(Enum):
    immediate = auto()  # '#'
    direct = auto()  # '$'
    indirect = auto()  # '@'
    predecrement_indirect = auto()  # '<'
    postincrement_indirect = auto()  # '>'


class Opcode(Enum):
    DAT = auto()
    MOV = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    JMP = auto()
    JMZ = auto()
    JMN = auto()
    DJN = auto()
    CMP = auto()
    SLT = auto()
    SPL = auto()


@dataclass(frozen=True, repr=True, unsafe_hash=True)
class Operation:
    opcode: Opcode
    modifier: OpcodeModifier


@dataclass(frozen=True, repr=True, unsafe_hash=True)
class Address:
    """
    An address is a combination of a mode and an expr in the grammar
    """
    addr: int  # TODO: add support for arithmetic expressions as well as constants
    mode: AddressingMode


@dataclass(frozen=True, repr=True, unsafe_hash=True)
class LabelAddress:
    addr: str  # a label that will eventually be turned into a number
    mode: AddressingMode


@dataclass(repr=True)
class Instruction:
    operation: Operation
    a: Address
    b: Address


@dataclass(frozen=True, repr=True, unsafe_hash=True)
class Label:
    text: str


@dataclass
class Warrior(repr=True):
    org: Address
    instructions: List[Instruction]
