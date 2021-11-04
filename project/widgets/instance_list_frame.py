from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)
from project.services.data_service import DataService
from project.widgets.instance_button import InstanceButton


class InstanceListFrame(QFrame):
    def __init__(self, main_window) -> None:
        super().__init__(main_window, objectName='frame')
        self.main_window = main_window
        self.buttons: list[InstanceButton] = []
        self.create_layout()
        self.refresh()

    def create_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        scroll = QScrollArea(objectName='scroll')
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        container = QWidget(objectName='container')
        scroll.setWidget(container)
        self.grid = QVBoxLayout(container)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

    def render_empty_button(self) -> None:
        btn_empty = QPushButton(
            QIcon(':add-icon'),
            'There are no instances registered. Click here to add a new one.',
            self,
            objectName='instance-button'
        )
        btn_empty.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_empty.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        btn_empty.clicked.connect(lambda: self.parent().add_action.trigger())
        self.grid.addWidget(btn_empty)

    def render_instances(self) -> None:
        data = DataService.get_data()
        self.buttons = []
        for instance in data.instances:
            btn = InstanceButton(self.main_window, self, instance)
            self.grid.addWidget(btn)
            self.buttons.append(btn)

    def deselect_instances(self) -> None:
        for btn in self.buttons:
            btn.set_deselected_style()

    def refresh(self) -> None:
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        if len(DataService.get_data().instances) == 0:
            self.render_empty_button()
        else:
            self.render_instances()
