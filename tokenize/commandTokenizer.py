from .simpleTokenizer import SimpleTokenizer


class CommandTokenizer(SimpleTokenizer):

    def __init__(self):
        super().__init__()

        self.add_pattern(True, 'Double Quoted Text', r'".*?"')
        self.add_pattern(True, 'Single Quoted Text', r"'.*?'")
        self.add_pattern(True, 'Text', r'[^\s\'\"]+')
        self.add_pattern(False, 'Whitespace', r'[\s\n]+')
