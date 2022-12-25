from enum import Enum
import platform
import re
import subprocess
from tokenize import CommandTokenizer


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

    @classmethod
    def _run_raw(cls, shell: Shell, command: str, **kwargs) -> str:

        subprocess_shell_param = None
        plat = WinShell.platform()

        if plat == Platform.WINDOWS:
            subprocess_shell_param = True
            if shell == Shell.CMD:
                command = re.sub('/', '\\/', command)
            elif shell == Shell.POWERSHELL:
                command = 'powershell ' + command
            elif shell == Shell.BASH:
                command = 'wsl.exe -- ' + command
            else:
                raise Exception(f'Error: class WinShell: _run(): Invalid Shell: {shell}')

        elif plat == Platform.WSL:
            subprocess_shell_param = False
            if shell == Shell.CMD:
                command = re.sub('/', '\\/', command)
                command = 'cmd.exe /c ' + command
            elif shell == Shell.POWERSHELL:
                command = 'powershell.exe -c ' + command
            elif shell == Shell.BASH:
                command = 'wsl.exe -- ' + command
            else:
                raise Exception(f'Error: class WinShell: _run(): Invalid Shell: {shell}')

        else:
            raise Exception(f'Error: class WinShell: _run(): Invalid Platform: {plat}')

        tokens = WinShell.command_tokenizer.tokenize(command)

        kwargs['stdout'] = subprocess.PIPE
        if 'shell' not in kwargs:
            kwargs['shell'] = subprocess_shell_param

        print(f'command: {command}')
        print(f'tokens: {tokens}')
        return subprocess.run(tokens, **kwargs).stdout.decode('utf-8')

    @classmethod
    def _run(cls, shell: Shell, command: str) -> str:
        # COMPLETE THE USERNAME FUNCTIONS FIRST
        # first go to the cwd
        # - may require finding the shell username
        # - may require converting a WSL to path to a Window path and vice-versa
        pass

    @classmethod
    def get_cmd_username(cls):
        return WinShell._run_raw(Shell.CMD, 'echo %USERNAME%').strip()

    @classmethod
    def get_powershell_username(cls):
        return WinShell._run_raw(Shell.POWERSHELL, 'echo $env:username').strip()

    @classmethod
    def get_bash_username(cls):
        return WinShell._run_raw(Shell.BASH, 'echo $USER').strip()

    @classmethod
    def cmd_raw(cls, command: str, **kwargs) -> str:
        return WinShell._run_raw(Shell.CMD, command, **kwargs)

    @classmethod
    def powershell_raw(cls, command: str, **kwargs) -> str:
        return WinShell._run_raw(Shell.POWERSHELL, command, **kwargs)

    @classmethod
    def bash_raw(cls, command: str, **kwargs) -> str:
        return WinShell._run_raw(Shell.BASH, command, **kwargs)

    @classmethod
    def platform(cls) -> Platform:
        plat = platform.platform()
        if 'Windows' in plat:
            return Platform.WINDOWS
        elif 'WSL' in plat:
            return Platform.WSL
        else:
            raise Exception('Error: class WinShell: platform(): Unexpected platform: {plat}')
