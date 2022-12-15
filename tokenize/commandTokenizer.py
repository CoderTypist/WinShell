import re
from typing import List, Union


class CommandToken:

    def __init__(self, match: re.Match):

        if not match:
            raise Exception('Error: class CommandToken: __init__(): match is None')

        self.text = match.groups()[0]
        self.length = len(self.text)


class CommandTokenizer:

    regex_double_quoted_text = re.compile(r'".*?"')
    regex_single_quoted_text = re.compile(r"'.*?'")
    regex_text = re.compile(r'[a-zA-Z]+[a-zA-Z0-9]*')
    regex_whitespace = re.compile(r'[\s\t]+')

    def tokenize(self, text: str) -> List[str]:

        if not text:
            raise Exception('Error: class CommandTokenizer: tokenize(): text is None')

        length = len(str)
        index = 0
        tokens = []

        while True:

            match = self.regex_double_quoted_text.match(text[index::])
            if match:
                token = CommandTokenizer.extract_token(match)
                tokens.append(token.text)
                index += token.length
                continue

            raise Exception(f'Error: class CommandTokenizer: tokenize(): Unable to tokenize: Invalid character(s): {text[index::]}')


    @classmethod
    def extract_token(cls, text: str, compiled_regex: re.Pattern) -> Union[None, CommandToken]:
        pass

