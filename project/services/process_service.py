import psutil
import os

from project.enums.process_status_enum import ProcessStatusEnum


class ProcessService:

    CE_PROCESS_NAME = 'ce.exe'
    LOBBY_PROCESS_NAME = 'lobby.exe'

    @classmethod
    def kill_ce_processes(cls) -> None:
        """
        Kill the ce.exe and lobby.exe processes
        """
        for p in psutil.process_iter():
            if p.name().lower() == ProcessService.CE_PROCESS_NAME:
                p.kill()
            if p.name().lower() == ProcessService.LOBBY_PROCESS_NAME:
                p.kill()
        print('Process ce.exe and lobby.exe killed!')

    @classmethod
    def get_ce_process_status(cls) -> ProcessStatusEnum:
        """
        Return the status of the ce.exe process
        """
        for p in psutil.process_iter():
            if p.name().lower() == ProcessService.CE_PROCESS_NAME:
                return ProcessStatusEnum.RUNNING
        return ProcessStatusEnum.STOPPED

    @classmethod
    def get_lobby_process_status(cls) -> ProcessStatusEnum:
        """
        Return the status of the lobby.exe process
        """
        for p in psutil.process_iter():
            if p.name().lower() == ProcessService.LOBBY_PROCESS_NAME:
                return ProcessStatusEnum.RUNNING
        return ProcessStatusEnum.STOPPED

    @classmethod
    def execute(cls, instance_path: str, command_line: str) -> None:
        """
        Execute the instance by command line
        """
        command_line = f'cd "{instance_path}" && {command_line}'
        ProcessService.kill_ce_processes()
        print(f'Executing command: {command_line}')
        os.system(command_line)
        ProcessService.kill_ce_processes()
