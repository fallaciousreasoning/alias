import os
import sys

ALIASES_DIRECTORY = 'aliases'
BAT_FILE_FORMAT = """
    @ECHO OFF
    {0} %* 2>&1
"""

def create_alias(command, alias, cd=None):
    d = ('' if cd is None else cd + '\\') + ALIASES_DIRECTORY
    if not os.path.exists(d):
        os.mkdir(d)

    with open(d + '\\' + alias + '.cmd', 'w') as f:
        f.write(BAT_FILE_FORMAT.format(command))

def print_help(filename):
    help_text = """
        Wrong number of parameters!
        Correct usage is:
            %s [command] [alias]
    """ % filename

    print(help_text)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(sys.argv)
        print_help(sys.argv[0])
        sys.exit(-1)

    create_alias(sys.argv[1], sys.argv[2], None if len(sys.argv) < 4 else sys.argv[3])
