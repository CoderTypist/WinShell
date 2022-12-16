import re
from typing import List, Union


class CommandToken:

    def __init__(self, match: re.Match):

        if not match:
            raise Exception('Error: class CommandToken: __init__(): match is None')

        self.text = match.group(0)
        self.length = len(self.text)


class CommandTokenizer:

    regex_double_quoted_text = re.compile(r'".*?"')
    regex_single_quoted_text = re.compile(r"'.*?'")
    regex_text = re.compile(r'[^\s\'\"]+')
    regex_whitespace = re.compile(r'[\s\n]+')

    @classmethod
    def tokenize(cls, text: str) -> List[str]:

        assert(isinstance(text, str))
        assert(len(text) > 0)
        if len(text) == 0:
            return []

        length = len(text)
        index = 0
        tokens = []

        while True:

            if index == length:
                break

            remaining_text = text[index::]
            # tokens to keep

            if (match := CommandTokenizer.regex_text.match(remaining_text)) or \
               (match := CommandTokenizer.regex_double_quoted_text.match(remaining_text)) or \
               (match := CommandTokenizer.regex_single_quoted_text.match(remaining_text)):

                token = CommandToken(match)
                tokens.append(token.text)
                index += token.length

            # tokens to ignore
            elif match := CommandTokenizer.regex_whitespace.match(remaining_text):
                token = CommandToken(match)
                index += token.length

            else:
                raise Exception(f'Error: class CommandTokenizer: tokenize(): Unable to tokenize: Invalid character(s): {text[index::]}')

        return tokens
