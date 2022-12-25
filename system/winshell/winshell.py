from enum import Enum
import platform
import re
import subprocess
from tokenize import CommandTokenizer


# Simply makes sure that commands are run in the correct shell
# Assumes CMD, PowerShell, and Bash are all available
# Assumes CMD is the default Windows Shell
# Assumes Bash is the default Linux Shell


command_tokenizer = CommandTokenizer()


class Platform(Enum):
    WINDOWS = 0
    WSL = 1


class Shell(Enum):
    CMD = 0
    POWERSHELL = 1
    BASH = 2


def _run_raw(shell: Shell, command: str, **kwargs) -> str:

    subprocess_shell_param = None
    plat = get_platform()

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

    tokens = command_tokenizer.tokenize(command)

    kwargs['stdout'] = subprocess.PIPE
    if 'shell' not in kwargs:
        kwargs['shell'] = subprocess_shell_param

    print(f'command: {command}')
    print(f'tokens: {tokens}')
    return subprocess.run(tokens, **kwargs).stdout.decode('utf-8')


def _run(shell: Shell, command: str) -> str:
    # COMPLETE THE USERNAME FUNCTIONS FIRST
    # first go to the cwd
    # - may require finding the shell username
    # - may require converting a WSL to path to a Window path and vice-versa
    pass


def cmd_raw(command: str, **kwargs) -> str:
    return _run_raw(Shell.CMD, command, **kwargs)


def powershell_raw(command: str, **kwargs) -> str:
    return _run_raw(Shell.POWERSHELL, command, **kwargs)


def bash_raw(command: str, **kwargs) -> str:
    return _run_raw(Shell.BASH, command, **kwargs)


def get_cmd_username():
    return _run_raw(Shell.CMD, 'echo %USERNAME%').strip()


def get_powershell_username():
    return _run_raw(Shell.POWERSHELL, 'echo $env:username').strip()


def get_bash_username():
    return _run_raw(Shell.BASH, 'echo $USER').strip()


def cwd(plat: Platform = None) -> None:
    if not plat:
        plat = get_platform()


def get_platform() -> Platform:
    plat = platform.platform()
    if 'Windows' in plat:
        return Platform.WINDOWS
    elif 'WSL' in plat:
        return Platform.WSL
    else:
        raise Exception('Error: class WinShell: platform(): Unexpected platform: {plat}')
