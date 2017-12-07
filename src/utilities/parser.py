# -*- coding: utf-8 -*-
""" File Parser

This module parses a text file and extracts transaction data to be used for
Simulating a transactional database

Options:
    -v  using this flag will print the output to stdout

Example:
    $ python parser.py <file_name> [-v]

"""
from objects.instruction import Instruction

class Parser:
    """ Parse the input file and store each line in instructions list """

    def __init__(self, file_name, logger):
        """ Parser Constructor """
        self.instructions = []
        self.logger = logger
        instruction_file = open(file_name, 'r')
        lines = instruction_file.readlines()
        instruction_file.close()
        instructions = []

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            logger.log("Line " + str(i+1) + ": " + line_stripped)

            if self.is_valid_instruction(line_stripped):
                instruction = line_stripped
                instructions.append(instruction)

        logger.log(instructions)

        self.instructions = list(reversed(instructions))

    def get_instruction(self):
        """ Get the next instruction to process """
        no_of_instructions = len(self.instructions)

        if no_of_instructions > 0:
            instruction = self.instructions.pop()
            return Instruction(instruction)

    def is_valid_instruction(self, value):
        """ Check value to see if it matches an approved instruction """

        operations = ['begin', 'W', 'R', 'end', 'dump', 'beginRO', 'fail', 'recover']

        return any(val in value for val in operations)
