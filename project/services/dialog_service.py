from PyQt5.QtWidgets import QInputDialog, QMessageBox


class DialogService:
    """
    Dialog renderization service
    """

    ###########################################################################
    # Messages
    ###########################################################################

    @classmethod
    def info(self, parent, message: str) -> None:
        """
        Render an information dialog
        """
        msg = QMessageBox()
        msg.information(parent, 'Info', message)

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

    ###########################################################################
    # Inputs
    ###########################################################################

    @classmethod
    def input(self, parent, message: str,
              text: str = None) -> tuple[str, bool]:
        """
        Render a text input dialog
        """
        text, ok = QInputDialog.getText(parent, 'Input', message, text=text)
        return text, ok

    @classmethod
    def input_int(self, parent, message: str,
                  value: int = 140) -> tuple[str, bool]:
        """
        Render a int input dialog
        """
        value, ok = QInputDialog.getInt(
            parent, 'Input', message, value=value, min=128, max=999
        )
        return value, ok

    @classmethod
    def combobox(self, parent, message: str,
                 items: list[str], current: str = None) -> tuple[str, bool]:
        """
        Render an combobox input dialog
        """
        current_index = None
        if current:
            for i, item in enumerate(items):
                if item == current:
                    current_index = i
                    break
        return QInputDialog().getItem(
            parent, 'Select', message, items, current_index, False
        )

    ###########################################################################
    # Questions
    ###########################################################################

    @classmethod
    def question(self, parent, message: str) -> bool:
        """
        Render a question dialog
        """
        msg = QMessageBox()
        answer = msg.question(parent, 'Question', message)
        return True if answer == QMessageBox.Yes else False
