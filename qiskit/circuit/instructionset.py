# -*- coding: utf-8 -*-

# Copyright 2017, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Instruction collection.
"""
from qiskit.exceptions import QiskitError
from .instruction import Instruction


class InstructionSet:
    """Instruction collection, and their contexts."""

    def __init__(self):
        """New collection of instructions.

        The context (qargs and cargs that each instruction is attached to),
        is also stored separately for each instruction.
        """
        self.instructions = []
        self.qargs = []
        self.cargs = []

    def __len__(self):
        """Return number of instructions in set"""
        return len(self.instructions)

    def __getitem__(self, i):
        """Return instruction at index"""
        return self.instructions[i]

    def add(self, gate, qargs, cargs):
        """Add an instruction and its context (where it's attached)."""
        if not isinstance(gate, Instruction):
            raise QiskitError("attempt to add non-Instruction" +
                              " to InstructionSet")
        self.instructions.append(gate)
        self.qargs.append(qargs)
        self.cargs.append(cargs)

    def inverse(self):
        """Invert all instructions."""
        for index, instruction in enumerate(self.instructions):
            self.instructions[index] = instruction.inverse()
        return self

    def q_if(self, *qregs):
        """Add controls to all instructions."""
        for gate in self.instructions:
            gate.q_if(*qregs)
        return self

    def c_if(self, classical, val):
        """Add classical control register to all instructions."""
        for gate in self.instructions:
            gate.c_if(classical, val)
        return self
