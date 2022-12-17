from abc import ABC
from enum import Enum
import platform
import subprocess
from tokenize import CommandTokenizer


class Platform(Enum):
    WINDOWS = 0
    WSL = 1


class Shell(Enum):
    CMD = 0
    POWERSHELL = 1
    SH = 2
    BASH = 3


# TODO: Change pwd? (e.g., def cd ...)
# TODO: Detect error values (would require changing return type from string to something else)
# Simply makes sure that commands are run in the correct shell
# Assumes CMD, PowerShell, sh and Bash are all available
# Assumes CMD is the default Windows Shell
# Assumes Bash is the default Linux Shell
class WinShell:

    command_tokenizer = CommandTokenizer()

    def __init__(self, shell: Shell, encoding, pwd: str = None):
        self.shell: Shell = shell
        self.encoding: str = encoding

    def run(self, command: str, **kwargs) -> str:
        return WinShell._run(self.shell, command, self.encoding, **kwargs)

    @classmethod
    def _run(cls, shell: Shell, command: str, encoding, **kwargs):

        subprocessShellParam = True

        if shell == Shell.CMD:
            # set subprocessShellParam (True or False) based on platform
            # set command, if any, to select shell
        elif shell == Shell.POWERSHELL:
            # set subprocessShellParam (True or False) based on platform
            # set command, if any, to select shell
        elif shell == Shell.SH:
            # set subprocessShellParam (True or False) based on platform
            # set command, if any, to select shell
        elif shell == Shell.BASH:
            # set subprocessShellParam (True or False) based on platform
            # set command, if any, to select shell
        else:
            raise Exception(f'Error: class WinShell: run(): Invalid Shell: {shell.name}')

        tokens = Shell.command_tokenizer.tokenize(command)
        kwargs['stdout'] = subprocess.PIPE
        kwargs['shell'] = subprocessShellParam
        return subprocess.run(tokens, **kwargs).stdout.decode(encoding)


    @classmethod
    def cmd(cls, command: str, encoding='utf-8', **kwargs) -> str:
        return WinShell._run(Shell.CMD, command, encoding, **kwargs)

    @classmethod
    def powershell(cls, command: str, encoding='utf-8', **kwargs) -> str:
        return WinShell._run(Shell.POWERSHELL, command, encoding, **kwargs)

    @classmethod
    def sh(cls, command: str, encoding='utf-8', **kwargs) -> str:
        return WinShell._run(Shell.SH, command, encoding, **kwargs)

    @classmethod
    def bash(cls, command: str, encoding='utf-8', **kwargs) -> str:
        return WinShell._run(Shell.BASH, command, encoding, **kwargs)

    @classmethod
    def platform(cls) -> Platform:
        pass

    @classmethod
    def encoding(cls, platform=None):
        if platform:
            pass
        else:
            pass

