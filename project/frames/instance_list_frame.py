from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from project.services.data_service import DataService
from project.widgets.instance_button import InstanceButton
from PyQt5.QtWidgets import (
    QFrame,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)


class InstanceListFrame(QFrame):
    """
    Instances list frame
    """

    def __init__(self, main_window) -> None:
        """
        Construct a new InstanceListFrame
        """
        super().__init__(main_window, objectName='frame')
        self.main_window = main_window
        self.buttons: list[InstanceButton] = []
        self._build()

    ###########################################################################
    # Build
    ###########################################################################

    def _build(self) -> None:
        """
        Build frame
        """
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        scroll = QScrollArea(objectName='scroll')
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        scroll_container = QWidget(objectName='container')
        scroll.setWidget(scroll_container)
        self._container = QVBoxLayout(scroll_container)
        self._container.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.refresh()

    def _build_empty_button(self) -> None:
        """
        Render empty instance list button
        """
        btn_empty = QPushButton(
            QIcon(':add-icon'),
            'There are no instances registered. Click here to add a new one.',
            self,
            objectName='instance-button'
        )
        btn_empty.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_empty.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        btn_empty.clicked.connect(
            lambda: self.main_window.add_action.trigger()
        )
        self._container.addWidget(btn_empty)

    def _build_instance_list(self) -> None:
        """
        Render instance list
        """
        self.buttons = []
        data = DataService.get_data()
        for instance in data.instances:
            btn = InstanceButton(self.main_window, self, instance)
            self._container.addWidget(btn)
            self.buttons.append(btn)

    ###########################################################################
    # Methods
    ###########################################################################

    def deselect_instances(self) -> None:
        """
        Deselect instances
        """
        for btn in self.buttons:
            btn.set_deselected_style()

    def refresh(self) -> None:
        """
        Refresh instance list
        """
        for i in reversed(range(self._container.count())):
            self._container.itemAt(i).widget().setParent(None)
        if len(DataService.get_data().instances) == 0:
            self._build_empty_button()
        else:
            self._build_instance_list()
