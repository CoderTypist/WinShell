import shlex
import subprocess
from system import Shell
from tokenize import CommandTokenizer


def main():
    example_command_tokenizer()
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

    print(Shell.run(shlex))


if __name__ == '__main__':
    main()
