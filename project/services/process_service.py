import psutil
import os


class ProcessService:

    @classmethod
    def kill_ce_and_lobby_process(cls) -> None:
        for p in psutil.process_iter():
            if p.name().lower() == 'ce.exe':
                p.kill()
            if p.name().lower() == 'lobby.exe':
                p.kill()
        print('Process ce.exe and lobby.exe killed!')

    @classmethod
    def execute(cls, instance_path: str, command_line: str) -> None:
        command_line = f'cd "{instance_path}" && {command_line}'
        ProcessService.kill_ce_and_lobby_process()
        print(f'Executing command: {command_line}')
        os.system(command_line)
        ProcessService.kill_ce_and_lobby_process()
