# -*- coding: utf-8 -*-
""" Replicated Concurrency Control and Recovery

    This application implements a distributed database using multiversion 
    Concurrency control, deadlock detection, replication, and failure recovery
"""
import sys
from src.transaction_manager import TransactionManager
from src.utilities.logger import Logger
from src.utilities.parser import Parser
from objects.site import Site
from src.objects.instruction import InstructionType

LOGGER = Logger()
SITES = []

def main():
    """ Main entry point for the application """

    if validate_args():
        # Python range function does not include last value so while there
        # Will only be 10 sites, the range must go to 11 to include 10
        for i in range(1, 11):
            site = Site(i, LOGGER)
            SITES.append(site)

        transaction_manager = TransactionManager(LOGGER)
        parser = Parser(sys.argv[1], LOGGER)

        instruction = parser.get_instruction()
        while instruction:
            if instruction.type == InstructionType.TRANSACTIONAL:
                transaction_manager.execute(instruction)
            else:
                # Execute on site from instruction
                pass

            instruction = parser.get_instruction()

def validate_args():
    """ Validate if the user arguments are valid """

    if len(sys.argv) < 2 or sys.argv[1] == '-v':
        print "To parse a file use the following command: parser.py <file_name> [-v]"
        return False

    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        print "Verbose set to true"
        LOGGER.show_stdout()

if __name__ == "__main__":
    main()
