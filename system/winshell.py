from enum import Enum
import platform
import re
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

    # *----------------------------*
    # | TESTED FOR MULT. COMMANDS  |
    # *----------------------------*
    # | SHELL      | Windows | WSL |
    # *----------------------------*
    # | cmd        | Yes     | No  |
    # | PowerShell | Yes     | No  |
    # | Bash       | Yes     | No  |
    # *----------------------------*

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
                command = 'cmd.exe /c ' + command
            elif shell == Shell.POWERSHELL:
                command = 'powershell.exe -c ' + command
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
        plat = WinShell.platform()
        out = WinShell._run_raw(Shell.CMD, 'echo %USERNAME%')
        if plat == Shell.WINDOWS:
            pass
        elif plat == Shell.WSL:
            pass
        else:
            raise Exception('Error: class WinShell: get_cmd_username(): Unexpected platform: {plat}')
        return out

    @classmethod
    def get_powershell_username(cls):
        pass

    '''
    @classmethod
    def get_bash_username(cls):
        pass
    '''

    @classmethod
    def cmd(cls, command: str, **kwargs) -> str:
        return WinShell._run_raw(Shell.CMD, command, **kwargs)

    @classmethod
    def powershell(cls, command: str, **kwargs) -> str:
        return WinShell._run_raw(Shell.POWERSHELL, command, **kwargs)

    @classmethod
    def bash(cls, command: str, **kwargs) -> str:
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
