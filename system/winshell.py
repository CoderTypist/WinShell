from enum import Enum
import platform
import subprocess
from tokenize import CommandTokenizer
from typing import Union


class Platform(Enum):
    WINDOWS = 0
    WSL = 1


class Shell(Enum):
    CMD = 0
    POWERSHELL = 1
    BASH = 2


# Simply makes sure that commands are run in the correct shell
# Assumes CMD, PowerShell, and Bash are all available
# Assumes CMD is the default Windows Shell
# Assumes Bash is the default Linux Shell
class WinShell:

    command_tokenizer = CommandTokenizer()

    def __init__(self, shell: Shell):
        self.shell: Shell = shell

    def run(self, command: str, **kwargs) -> str:
        return WinShell._run(self.shell, command, **kwargs)

    @classmethod
    def _run(cls, shell: Shell, command: str, **kwargs) -> Union[str, bytes]:

        subprocess_shell_param = None
        plat = WinShell.platform()

        if plat == Platform.WINDOWS:
            subprocess_shell_param = True
            if shell == Shell.CMD:
                pass
            elif shell == Shell.POWERSHELL:
                command = 'powershell;' + command
            elif shell == Shell.BASH:
                command = 'wsl.exe -- ' + command
            else:
                raise Exception(f'Error: class WinShell: _run(): Invalid Shell: {shell}')

        elif plat == Platform.WSL:
            subprocess_shell_param = False
            if shell == Shell.CMD:
                pass
            elif shell == Shell.POWERSHELL:
                pass
            elif shell == Shell.BASH:
                pass
            else:
                raise Exception(f'Error: class WinShell: _run(): Invalid Shell: {shell}')

        else:
            raise Exception(f'Error: class WinShell: _run(): Invalid Platform: {plat}')

        tokens = WinShell.command_tokenizer.tokenize(command)

        kwargs['stdout'] = subprocess.PIPE
        if 'shell' not in kwargs:
            kwargs['shell'] = subprocess_shell_param

        return subprocess.run(tokens, **kwargs).stdout.decode('utf-8')

    @classmethod
    def cmd(cls, command: str, **kwargs) -> str:
        return WinShell._run(Shell.CMD, command, **kwargs)

    @classmethod
    def powershell(cls, command: str, **kwargs) -> str:
        return WinShell._run(Shell.POWERSHELL, command, **kwargs)

    @classmethod
    def bash(cls, command: str, **kwargs) -> str:
        return WinShell._run(Shell.BASH, command, **kwargs)

    @classmethod
    def platform(cls) -> Platform:
        plat = platform.platform()
        if 'Windows' in plat:
            return Platform.WINDOWS
        elif 'WSL' in plat:
            return Platform.WSL
        else:
            raise Exception('Error: class WinShell: platform(): Unexpected platform: {plat}')

    @classmethod
    def platform_encoding(cls, platform: Platform=None) -> str:
        plat = platform if platform else WinShell.platform()
        if plat == Platform.WINDOWS:
            return 'utf-16'
        elif plat == Platform.WSL:
            return 'utf-8'
        else:
            raise Exception('Error: class WinShell: encoding(): Unexpected platform: {plat}')
