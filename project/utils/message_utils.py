from PyQt6.QtWidgets import QMessageBox, QWidget


def show_error(message: str, title: str = "Error!", parent: QWidget | None = None) -> None:
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()


def show_info(message: str, title: str = "Info", parent: QWidget | None = None) -> None:
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()
