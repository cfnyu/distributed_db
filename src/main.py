# -*- coding: utf-8 -*-
""" Replicated Concurrency Control and Recovery

    This application implements a distributed database using multiversion 
    Concurrency control, deadlock detection, replication, and failure recovery
"""
import sys
import os.path
from transaction_manager import TransactionManager
from utilities.logger import Logger
from utilities.parser import Parser

LOGGER = Logger()
SITES = []

def main():
    """ Main entry point for the application """

    if validate_args():
        # Confirm time with professor
        transaction_manager = TransactionManager(LOGGER)
        parser = Parser(sys.argv[1], LOGGER)

        instruction = parser.get_instruction()
        while instruction:
            transaction_manager.execute(instruction)
            instruction = parser.get_instruction()

def validate_args():
    """ Validate if the user arguments are valid """
    file_path = sys.argv[1]

    if len(sys.argv) < 2 or file_path == '-v':
        print "To parse a file use the following command: main.py <file_name> [-v]"
        return False

    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        print "Verbose set to true"
        LOGGER.show_stdout()

    if not os.path.exists(file_path):
        print "'%s' not found" % file_path
        return False

    return True

if __name__ == "__main__":
    main()
