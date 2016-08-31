import os
import sys

import re

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

def list_aliases(cd=None):    
    d = ('' if cd is None else cd + '\\') + ALIASES_DIRECTORY
    if not os.path.exists(d):
        os.mkdir(d)

    pattern = re.compile('\s?(.*) %\* 2>&1')
    files = [file for file in os.listdir(d) if file.endswith('.cmd')]

    longest_command = 0
    longest_alias = 0

    aliases = []
    commands = []

    for file in files:
        text = None
        with open(d + '\\' + file) as f:
            text = f.read()
        match = re.findall(pattern, text)
        command = match[0].strip()

        aliases.append(file[:-4])
        commands.append(command)

        longest_alias = max(longest_alias, len(aliases[-1]))
        longest_command = max(longest_command, len(commands[-1]))

    row_format = "{:<" + str(longest_command + 4) + "}" + "{:<" + str(longest_alias + 4) + "}"
    print(row_format.format("Command", "Alias"))

    for i in range(len(aliases)):
        print(row_format.format(commands[i], aliases[i]))

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
