from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


def hide_items_in_list(items: list):
	for item in items:
		item.hide()


class QExtendedLabel(QLabel):
	clicked = pyqtSignal()

	def setBlurred(self, blur_strength: int):
		self.blur = QGraphicsBlurEffect()
		self.blur.setBlurRadius(blur_strength)
		self.setGraphicsEffect(self.blur)

	def setOpacity(self, opacity: int):
		self.opacity = QGraphicsOpacityEffect()
		self.opacity.setOpacity(opacity / 100)
		self.setGraphicsEffect(self.opacity)

	def toggle(self):
		if self.isHidden():
			self.show()
		else:
			self.hide()

	def mousePressEvent(self, ev):
		self.clicked.emit()


class QSimpleRectangle(QExtendedLabel):
	def __init__(self, *__args):
		super().__init__(*__args)

	def setRectangle(self, x: int, y: int, width: int, height: int, stylesheet: str):
		self.move(x, y)
		self.setFixedSize(width, height)
		self.setStyleSheet(stylesheet)


class QSimpleImage(QExtendedLabel):
	def __init__(self, *__args):
		super().__init__(*__args)

	def setImage(self, source: str, x: int, y: int, width: int, height: int):
		pic = QLabel(self)
		pic.setPixmap(QPixmap(source))
		pic.setScaledContents(True)
		pic.setFixedSize(width, height)
		pic.move(x, y)


class QExtendedButton(QPushButton):
	def __init__(self, *__args):
		super().__init__(*__args)
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


class QErrorDialog(QMessageBox):
	def __init__(self, message: str = "Invalid Operation!", title: str = "Error"):
		super().__init__()

		self.resize(300, 250)
		self.setWindowTitle(title)
		self.setIcon(QMessageBox.Icon.Critical)

		dialog = QMessageBox(parent=self, text=message)
		dialog.setWindowTitle(title)
		dialog.setIcon(dialog.Icon.Critical)
		dialog.exec()
