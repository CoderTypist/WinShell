from abc import ABC
from dataclasses import dataclass
import re
from typing import List


@dataclass
class TokenPattern:
    keep: bool
    name: str
    pattern: re.Pattern


class SimpleTokenizer(ABC):

    def __init__(self):
        self.token_patterns: List[TokenPattern] = []

    def add_pattern(self, keep: bool, name: str, pattern: str) -> None:
        self.token_patterns.append(TokenPattern(keep, name, re.compile(fr'{pattern}')))

    def tokenize(self, text: str) -> List[str]:

        if len(text) == 0:
            return []

        length = len(text)
        index = 0
        tokens = []

        # keep extracting tokens until the entire string is processed
        while True:

            # text has been completely processed
            if index == length:
                break

            # extract the substring containing the unprocessed text
            remaining_text = text[index::]

            # check all compiled regex patterns in order
            for tp in self.token_patterns:

                # try to match the substring against the current pattern
                match = tp.pattern.match(remaining_text)

                # if a match was found, add the token to the list of tokens
                if match:
                    val = match.group(0)
                    index += len(val)
                    if tp.keep:
                        tokens.append(val)
                    break
            # substring did not match with any pattern (i.e., unexpected characters or sequence of characters)
            else:
                raise Exception(
                    f'Error: class CommandTokenizer: tokenize(): Unable to tokenize: Invalid character(s): {text[index::]}')

        return tokens
