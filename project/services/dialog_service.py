from PyQt5.QtWidgets import QInputDialog, QMessageBox


class DialogService:
    """
    Dialog renderization service
    """

    @classmethod
    def question(self, parent, message: str) -> bool:
        """
        Render a question dialog
        """
        msg = QMessageBox()
        answer = msg.question(parent, 'Question', message)
        return True if answer == QMessageBox.Yes else False

    @classmethod
    def info(self, parent, message: str) -> None:
        """
        Render an information dialog
        """
        msg = QMessageBox()
        msg.information(parent, 'Info', message)

    @classmethod
    def input(self, parent, message: str,
              text: str = None) -> tuple[str, bool]:
        """
        Render a text input dialog
        """
        text, ok = QInputDialog.getText(parent, 'Input', message, text=text)
        return text, ok

    @classmethod
    def warning(self, parent, message: str) -> None:
        """
        Render an warning dialog
        """
        msg = QMessageBox()
        msg.warning(parent, 'Warning', message)

    @classmethod
    def error(self, parent, message: str) -> None:
        """
        Render an error dialog
        """
        msg = QMessageBox()
        msg.critical(parent, 'Error', message)
