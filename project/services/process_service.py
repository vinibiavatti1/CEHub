import psutil


class ProcessService:

    @classmethod
    def kill_ce_and_lobby_process(cls) -> None:
        for p in psutil.process_iter():
            if p.name().lower() == 'ce.exe':
                p.kill()
            if p.name().lower() == 'lobby.exe':
                p.kill()
