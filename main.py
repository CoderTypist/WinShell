from system import Shell
from system import WinShell
from tokenize import CommandTokenizer
import os


# TODO: 01: Test for multiple shell commands on Platform.WSL
# TODO: 02: Username functions
# TODO: 03: _run

def main():

    example_command_tokenizer()
    # example_username()
    example_shell()



def header(title):
    print('---------------------------------------------------------')
    print(f'{title}:')


def example_command_tokenizer():

    text = './script.py arg1 "arg with spaces" \'another arg with spaces\' arg4'

    tokenizer = CommandTokenizer()
    try:
        tokens = tokenizer.tokenize(text)
        for t in tokens:
            print(f'- {t}')
    except Exception as e:
        print(e)


'''
def example_username():

    header('CMD - username')
    print(WinShell.get_cmd_username())

    header('POWERSHELL - username')
    print(WinShell.get_powershell_username())

    header('BASH - username')
    print(WinShell.get_powershell_username())
'''


def example_shell():

    header('CMD - class method')
    print(WinShell.cmd('dir /ah & echo %cd% & dir /ah'))

    header('POWERSHELL - class method')
    print(WinShell.powershell('dir -Force ./ ; Get-Location ; dir -Force ./'))

    header('BASH - class method')
    # print(WinShell.bash('ls; pwd; ls'))
    print(WinShell.bash('ls -la ./ ; pwd ; ls -la ./'))


if __name__ == '__main__':
    main()
