# contents:
# get_possible_passwords()
# check_lengths(list)
# sum_list(list)
# hamming(str, str)
# assemble_database

from statistics import mode as mode
from statistics import variance as variance
from statistics import StatisticsError as StatisticsError


def get_possible_passwords():

    list_of_passwords = []

    print('> Enter all possible passwords.')
    print('> When done, enter "end".')
    print('> If you want to clear the latest input, enter "del".')
    print('> ')

    while True:

        latest_password = str(input('> ').upper())

        if latest_password == 'DEL':
            if len(list_of_passwords) >= 1:
                print('> Deleted "{}".'.format(list_of_passwords[-1]))
                list_of_passwords.remove(list_of_passwords[-1])
            else:
                print('> Error: no passwords in memory.')

        elif latest_password == 'END':
            break

        elif latest_password.isalpha() is False:
            print('> Error: please input alphabetical characters only.')
            continue

        elif latest_password in list_of_passwords:
            print('> Error: entered duplicate password.')

        else:
            list_of_passwords.append(latest_password)

    list_of_passwords = check_lengths(list_of_passwords)

    if list_of_passwords is False:
        exit(1)
    return list_of_passwords


def check_lengths(list_of_passwords):
    """Recursive function: calculates the mode of input string lengths.
    Prompts user to correct faulty inputs if entries that do not match mode are found.
    In case of a tie in lengths (no mode can be calculated), the program terminates.
    When no variance is found, returns the list of passwords."""

    len_bank = []

    for i in list_of_passwords:
        len_bank.append(len(i))

    if variance(len_bank) == 0:
        return list_of_passwords

    try:
        len_mode = mode(len_bank)
    # mode couldn't be calculated.
    except StatisticsError:
        print('> Error: program detected multiple errors in entries. Please try again.')
        return False

    for i in list_of_passwords:
        if len(i) != len_mode:
            print('> Error: program detected a password of inconsistent length: "{}"'.format(i))
            print('> Please enter correction:')

            list_of_passwords.remove(i)

            while True:
                password_correction = str(input('> ').upper())

                if password_correction.isalpha() is False:
                    print('> Error: please input alphabetical characters only.')
                    continue

                else:
                    list_of_passwords.append(password_correction)
                    break

    check_lengths(list_of_passwords)
    return list_of_passwords


def sum_list(l1):
    s = 0
    for i in l1:
        s += i
    return s


def hamming(s1, s2):
    # from https://pythonadventures.wordpress.com/2010/10/19/hamming-distance/
    assert len(s1) == len(s2)
    return sum(ch1 == ch2 for ch1, ch2 in zip(s1, s2))


def assemble_database(passwords):
    """
    :param passwords: a list of passwords.
    :return: for example: {'password1': {'password2': 0, 'password3': 3}, 'password2' : {...}, 'password3': {...}}
    basically a dict that contains reversed Hamming distances for everything.
    """

    database = {}

    for entry in passwords:
        database[entry] = {}

    for key in database.keys():
        for entry in passwords:
            # Don't add a password to it's own list.
            if entry != key:
                database[key][entry] = hamming(key, entry)

    return database


def attempt_crack(database):

    while True:

        # Now, we make a guess for the try. It is the most beneficial to choose a word
        # that has many similar words. For example, if the options are as follows:
        # GATE GAME GAZE HEAD TREE
        # We would choose one of the first three words.
        highest_similarities = {}
        # Take a sum of all hamming numbers for each password.
        # <highest_similarities> will be reduced to {'PASSWORD': sum}
        for key in database:
            highest_similarities[key] = sum_list(sorted(database[key].values()))

        # This will be the guess.
        guess = max(highest_similarities.keys(), key=(lambda k: highest_similarities[k]))

        print('> Try "{}".'.format(guess))
        print('> Enter similarity if not correct. Enter "exit" if ready.')

        while True:
            similarity = input('> ')
            if similarity.isnumeric() is True:
                break
            elif similarity.upper() == 'EXIT':
                print('> Goodbye!')
                return
            else:
                print('> Error: please enter a number.')

        new_database = {}

        # Delete words that are surely not correct.
        for entry in database[guess]:
            if entry in database:
                if guess in database[entry]:
                    # Delete the latest guess from other possibilities' lists.
                    del database[entry][guess]
                if database[guess][entry] == int(similarity):
                    # Keep the words that match the user-given number.
                    new_database[entry] = database[entry]

        database = new_database
