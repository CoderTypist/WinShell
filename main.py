from system import WinShell
from tokenize import CommandTokenizer


# TODO: 01: _run


def main():

    example_command_tokenizer()
    example_shell_raw()
    example_username()


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


def example_shell_raw():

    header('_cmd_raw()')
    print(WinShell.cmd_raw('dir /ah & echo %cd% & dir /ah'))

    header('_powershell_raw()')
    print(WinShell.powershell_raw('dir -Force ./ ; Get-Location ; dir -Force ./'))

    header('_bash_raw()')
    print(WinShell.bash_raw('ls -la ./ ; pwd ; ls -la ./'))


def example_username():

    header('CMD - username')
    uname = WinShell.get_cmd_username()
    print('####################')
    print(f'X-{uname}-X')
    print('####################')

    header('POWERSHELL - username')
    uname = WinShell.get_powershell_username()
    print('####################')
    print(f'X-{uname}-X')
    print('####################')

    print(WinShell.bash_raw('uname -a'))
    header('POWERSHELL - username')
    uname = WinShell.get_bash_username()
    print('####################')
    print(f'X-{uname}-X')
    print('####################')


if __name__ == '__main__':
    main()
