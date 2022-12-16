from tokenize import CommandTokenizer


def main():
    pass


if __name__ == '__main__':

    text = './script.py arg1 "arg with spaces" \'another arg with spaces\' arg4'

    try:
        tokens = CommandTokenizer.tokenize(text)
        for t in tokens:
            print(f'- {t}')
    except Exception as e:
        print(e)


    main()

