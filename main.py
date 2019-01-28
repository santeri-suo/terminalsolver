# A tool for solving passwords for terminals in Fallout games.
# By @santeri-suo
# Date of last change: 11.08.2018

import functions


def main():

    print('> RobCo terminal password cracker v0.1')
    print('> ')
    possible_passwords = functions.get_possible_passwords()
    print('> ')
    print('> Passwords entered.')
    print('> ')

    database = functions.assemble_database(possible_passwords)
    functions.attempt_crack(database)


main()
