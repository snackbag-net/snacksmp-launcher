import os

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
import snackbag.helper as h
from pathlib import Path
from snackbag.qtextension import *
import ssl
import json
import urllib.request


class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.version = "Beta 1.0.0/Darwin"
		self.setFixedSize(960, 540)
		self.setWindowTitle("SnackSMP Launcher")
		self.user = "JX_Snack"
		self.rank = "Lead Developer"
		self.buttons = []
		self.reload_app()
		self.sidebar()
		self.setup_btns()

	def sidebar(self):
		rect = QSimpleRectangle(self)
		rect.setRectangle(0, 0, 200, 540, "background-color: #1e1e1e;")

		name = QExtendedLabel(self)
		name.move(80, 15)
		name.setStyleSheet("color: white; font-size: 16px; font-family: \"Futura\"; font-style: bold;")
		name.setText(self.user)

		rank = QExtendedLabel(self)
		rank.move(80, 35)
		rank.setStyleSheet("color: gray; font-size: 12px; font-family: \"Futura\";")
		rank.setText(self.rank)

		uuid = h.webreq(f"https://api.minetools.eu/uuid/{self.user}")
		uuid = json.loads(uuid)['id']
		user_icn_url = f'https://skins.mcstats.com/skull/{uuid}'
		user_icn_data = urllib.request.urlopen(user_icn_url).read()

		user_icn_img = QImage()
		user_icn_img.loadFromData(user_icn_data)

		user_icn = QLabel(self)
		user_icn.setScaledContents(True)
		user_icn.setFixedSize(int(100 / 1.5), int(90 / 1.5))
		user_icn.move(10, 10)
		user_icn.setPixmap(QPixmap(user_icn_img))

		# Play
		play_icn = QLabel(self)
		play_icn.setScaledContents(True)
		play_icn.setFixedSize(60, 60)
		play_icn.move(10, 90)
		play_icn.setPixmap(QPixmap("snackbag/storage/play_large.png"))

		self.play_text = QLabel(self)
		self.play_text.setText("Play")
		self.play_text.setStyleSheet(h.load_stylesheet(True)["launcher_name_selected"])
		self.play_text.move(75, 107)
		self.play_text.setFixedWidth(200)
		self.play_text.adjustSize()

		self.play_btn = QPushButton(self)
		self.play_btn.setText("")
		self.play_btn.move(0, 90)
		self.play_btn.setFixedSize(200, 60)
		self.play_btn.clicked.connect(lambda null=None: self.switch_page("play"))

		# Changelog
		changelog_icn = QLabel(self)
		changelog_icn.setScaledContents(True)
		changelog_icn.setFixedSize(60, 60)
		changelog_icn.move(10, 150)
		changelog_icn.setPixmap(QPixmap("snackbag/storage/changelog_large.png"))

		self.changelog_text = QLabel(self)
		self.changelog_text.setText("Changelog")
		self.changelog_text.setStyleSheet(h.load_stylesheet(True)["launcher_name"])
		self.changelog_text.move(75, 167)
		self.changelog_text.setFixedWidth(200)
		self.changelog_text.adjustSize()

		self.changelog_btn = QPushButton(self)
		self.changelog_btn.setText("")
		self.changelog_btn.move(0, 150)
		self.changelog_btn.setFixedSize(200, 60)
		self.changelog_btn.clicked.connect(lambda null=None: self.switch_page("changelog"))

		# Settings
		settings_icn = QLabel(self)
		settings_icn.setScaledContents(True)
		settings_icn.setFixedSize(60, 60)
		settings_icn.move(10, 450)
		settings_icn.setPixmap(QPixmap("snackbag/storage/settings_large.png"))

		self.settings_text = QLabel(self)
		self.settings_text.setText("Settings")
		self.settings_text.setStyleSheet(h.load_stylesheet(True)["launcher_name"])
		self.settings_text.move(75, 466)
		self.settings_text.setFixedWidth(200)
		self.settings_text.adjustSize()

		self.settings_btn = QPushButton(self)
		self.settings_btn.setText("")
		self.settings_btn.move(0, 450)
		self.settings_btn.setFixedSize(200, 60)
		self.settings_btn.clicked.connect(lambda null=None: self.switch_page("settings"))

		self.buttons.append(self.play_btn)
		self.buttons.append(self.changelog_btn)
		self.buttons.append(self.settings_btn)

		version_number = QExtendedLabel(self)
		version_number.setText(self.version)
		version_number.move(10, 510)
		version_number.setMinimumWidth(1000)
		version_number.setStyleSheet(h.load_stylesheet(True)["version_label"])

	def playUI(self):
		elems = []

		# Image background Button
		self.img_bg = QLabel(self)
		self.img_bg.setScaledContents(True)
		filepath = Path("snackbag") / Path("storage") / Path("launcher_bg.png")

		self.img_bg.setFixedSize(1200, 360)
		self.img_bg.move(0, 90)
		self.img_bg.setPixmap(QPixmap(str(filepath)))
		elems.append(self.img_bg)

		# Play button
		self.large_play_icn = QLabel(self)
		self.large_play_icn.setScaledContents(True)
		self.large_play_icn.setFixedSize(240, 55)
		self.large_play_icn.move(480, 435)
		self.large_play_icn.setPixmap(QPixmap(str(Path("snackbag") / Path("storage") / Path("play_button.png"))))
		self.large_play_icn.enterEvent = lambda null=None: self.plabHover()
		self.large_play_icn.leaveEvent = lambda null=None: self.plabUnHover()
		self.buttons.append(self.large_play_icn)
		elems.append(self.large_play_icn)

		# Play part
		self.plab = QExtendedLabel(self)
		self.plab.setText("Play")
		self.plab.move(210, 50)
		self.plab.setStyleSheet(h.load_stylesheet(True)["launcher_part_selected"])
		elems.append(self.plab)

		# Modpack part
		mlab = QExtendedLabel(self)
		mlab.setText("Modpack")
		mlab.move(260, 50)
		mlab.setStyleSheet(h.load_stylesheet(True)["launcher_part"])
		elems.append(mlab)

		self.pages["play"][1] = elems

	def changelogUI(self):
		elems = []

		test = QExtendedLabel(self)
		test.setText("Test")
		test.move(210, 50)
		elems.append(test)

		self.pages["changelog"][1] = elems

	def settingsUI(self):
		elem = self.pages["settings"][1]

	def plabHover(self):
		self.large_play_icn.move(480, 437)

	def plabUnHover(self):
		self.large_play_icn.move(480, 435)

	def switch_page(self, page):
		if self.current_page is not None:
			for element in self.pages[self.current_page][1]:
				element.hide()

		self.current_page = page

		for element in self.pages[page][1]:
			element.show()

	def reload_app(self):
		# Download background image
		h.img_webreq(h.secondary_api_path + "/background.png", "launcher_bg.png")

		self.pages = {
			"play": [self.playUI, []],
			"changelog": [self.changelogUI, []],
			"settings": [self.settingsUI, []]
		}
		self.current_page = None
		self.playUI()
		self.switch_page("play")
		self.changelogUI()
		self.switch_page("changelog")
		self.settingsUI()
		self.switch_page("settings")

		self.switch_page("play")

	def setup_btns(self):
		for button in self.buttons:
			button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


def run():
	# We go YOLO mode
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	ssl._create_default_https_context = ssl._create_unverified_context
	h.ctx = ctx

	app = QApplication(sys.argv)
	font_id = QFontDatabase.addApplicationFont(str(Path(os.getcwd()) / Path("snackbag") / Path("Futura.ttf")))
	font_id2 = QFontDatabase.addApplicationFont(str(Path(os.getcwd()) / Path("snackbag") / Path("Futura Bold.ttf")))

	if font_id < 0 or font_id2 < 0:
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Icon.Critical)
		msg.setText("Could not load font(s). Please report this issue!")
		msg.exec()
		sys.exit(0)

	app.setStyleSheet(h.load_stylesheet())
	window = Window()
	window.show()
	sys.exit(app.exec())
