import os
import sys

import re

from pathlib import Path

ALIASES_DIRECTORY = 'aliases'
BAT_FILE_FORMAT = """
    @ECHO OFF
    {0} %* 2>&1
"""

def get_dir(cd=None):
    print(cd)
    path = os.path.join(cd or '', ALIASES_DIRECTORY)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_alias(alias, command, cd=None):
    d = get_dir(cd)
    with open(f'{d}\\{alias}.cmd', 'w') as f:
        f.write(BAT_FILE_FORMAT.format(command))

def delete_alias(alias, cd=None):
    d = get_dir(cd)
    os.remove(f'{d}\\{alias}.cmd')

def list_aliases(cd=None):    
    d = get_dir(cd)
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

        longest_alias = max(longest_alias, len(aliases[-1]), len("Alias"))
        longest_command = max(longest_command, len(commands[-1]), len("Command"))

    row_format = "{:<" + str(longest_alias + 4) + "}" + "{:<" + str(longest_command + 4) + "}"
    print(row_format.format("Alias", "Command"))

    for i in range(len(aliases)):
        print(row_format.format(aliases[i], commands[i]))

def print_help():
    name = Path(__file__).name
    help_text = f"""
        Wrong number of parameters!
        Correct usage is:
            {name} [alias] [command]
        or
            {name} --list
        or
            {name} --delete [alias]
    """

    print(help_text)

if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)

    if '--list' in sys.argv or '-l' in sys.argv:
        list_aliases(cur_dir)
        sys.exit(0)

    if '--delete' in sys.argv or '-D' in sys.argv:
        delete_alias(sys.argv[2], cur_dir)
        sys.exit(0)

    if len(sys.argv) < 3:
        print(sys.argv)
        print_help(sys.argv[0])
        sys.exit(-1)

    create_alias(sys.argv[1], sys.argv[2], cur_dir)
