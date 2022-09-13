import threading
from typing import Any, Callable, Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QProgressDialog,
    QProgressBar,
    QApplication,
)


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

    ###########################################################################
    # Progress
    ###########################################################################

    @classmethod
    def progress(cls, parent: Any, message: str, action: Callable[[], None],
                 cancel_button_label: Optional[str] = None) -> None:
        """
        Show a progress bar dialog and process action in thread.
        """
        dialog = QProgressDialog(
            message, 'cancel btn', 0, 0, parent
        )
        if cancel_button_label is not None:
            dialog.setCancelButtonText(cancel_button_label)
        else:
            dialog.setCancelButton(None)
        bar = QProgressBar(dialog)
        bar.setTextVisible(False)
        bar.setMinimum(0)
        bar.setMaximum(0)
        dialog.setBar(bar)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)
        thread = threading.Thread(target=action)
        dialog.show()
        thread.start()
        while thread.is_alive():
            QApplication.processEvents()
        dialog.close()
