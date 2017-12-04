# -*- coding: utf-8 -*-
""" Replicated Concurrency Control and Recovery

    This application implements a distributed database using multiversion 
    Concurrency control, deadlock detection, replication, and failure recovery
"""
import sys
from src.transaction_manager import TransactionManager
from src.utilities.logger import Logger
from src.utilities.parser import Parser

def main():
    """ Main entry point for the application """
    
    if len(sys.argv) < 2 or sys.argv[1] == '-v':
        print "To parse a file use the following command: parser.py <file_name> [-v]"
        return False

    logger = Logger()

    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        print "Verbose set to true"
        logger.show_stdout()

    transaction_manager = TransactionManager(logger)
    parser = Parser(sys.argv[1], logger)

    instruction = parser.get_instruction()
    while instruction:
        transaction_manager.execute(instruction)
        instruction = parser.get_instruction()

if __name__ == "__main__":
    main()
