import sys


def get_int(message):
    while True:
        val = raw_input(message)

        try:
            return int(val)
        except ValueError:
            continue


def get_choice(valid_choices):

    while True:
        val = get_int("")

        if val in valid_choices:
            return val
        else:
            print "Invalid choice.  Valid choices: {}".format(valid_choices)


def export_to_file(filename, func_to_output, *args):
    stdout = sys.stdout
    sys.stdout = open(filename, 'w+')
    func_to_output(*args)
    sys.stdout = stdout

