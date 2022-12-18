from system import Shell
from system import WinShell
from tokenize import CommandTokenizer


def main():

    # example_command_tokenizer()
    example_shell()


def example_command_tokenizer():

    text = './script.py arg1 "arg with spaces" \'another arg with spaces\' arg4'

    tokenizer = CommandTokenizer()
    try:
        tokens = tokenizer.tokenize(text)
        for t in tokens:
            print(f'- {t}')
    except Exception as e:
        print(e)


def example_shell():

    def header(title):
        print('---------------------------------------------------------')
        print(f'{title}:')

    header('CMD - class method')
    print(WinShell.cmd('dir'))

    header('CMD - object')
    shell = WinShell(Shell.CMD)
    print(shell.run('dir'))

    header('POWERSHELL - class method')
    print(WinShell.powershell('dir'))

    header('POWERSHELL - object')
    shell = WinShell(Shell.POWERSHELL)
    print(shell.run('dir'))

    header('BASH - class method')
    print(WinShell.bash('ls'))

    header('BASH - object')
    shell = WinShell(Shell.BASH)
    print(shell.run('ls'))


if __name__ == '__main__':
    main()
