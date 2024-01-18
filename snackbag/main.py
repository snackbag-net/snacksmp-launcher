import copy
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

		self.storage_path = Path("snackbag") / Path("storage")
		self.furnace_icon = self.storage_path / Path("furnace_3d.png")
		self.crafting_table_icon = self.storage_path / Path("crafting_table_3d.png")
		self.sand_icon = self.storage_path / Path("sand_3d.png")

		self.modpack_info = h.webreq(f"{h.secondary_api_path}/../modpack.json")
		self.modpack_info = json.loads(self.modpack_info)
		self.active_modpack = self.modpack_info["latest"]
		self.active_modpack_info = self.modpack_info["all"][self.active_modpack]
		print(self.active_modpack_info)

		self.reload_app()
		self.sidebar()
		self.setup_btns()

	def sidebar(self):
		rect = QSimpleRectangle(self)
		rect.setRectangle(0, 0, 200, 540, "background-color: #1a1a1a;")

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

		# Big cool bold text thingies
		self.pages["play"].append(self.play_text)
		self.pages["changelog"].append(self.changelog_text)
		self.pages["settings"].append(self.settings_text)

	def playUI(self):
		elems = []

		# Image background Button
		self.img_bg = QLabel(self)
		self.img_bg.setScaledContents(True)
		filepath = self.storage_path / Path("launcher_bg.png")

		self.img_bg.setFixedSize(1200, 360)
		self.img_bg.move(0, 90)
		self.img_bg.setPixmap(QPixmap(str(filepath)))
		elems.append(self.img_bg)

		# Play button
		self.large_play_icn = QLabel(self)
		self.large_play_icn.setScaledContents(True)
		self.large_play_icn.setFixedSize(240, 55)
		self.large_play_icn.move(480, 435)
		self.large_play_icn.setPixmap(QPixmap(str(self.storage_path / Path("play_button.png"))))
		self.large_play_icn.enterEvent = lambda null=None: self.plabHover()
		self.large_play_icn.leaveEvent = lambda null=None: self.plabUnHover()
		self.buttons.append(self.large_play_icn)
		elems.append(self.large_play_icn)

		# Modpack icon
		self.modpack_icn = QLabel(self)
		self.modpack_icn.setScaledContents(True)
		filepath = self.storage_path / Path("unknown_texture.png")

		self.modpack_icn.setFixedSize(48, 48)
		self.modpack_icn.move(200, 455)
		self.modpack_icn.setPixmap(QPixmap(str(filepath)))
		elems.append(self.modpack_icn)

		self.modpack_title = QExtendedLabel(self)
		self.modpack_title.setText(f"Critical Error")
		self.modpack_title.move(250, 460)
		self.modpack_title.setStyleSheet(h.load_stylesheet(True)["modpack_title"])
		self.modpack_title.adjustSize()

		self.modpack_desc = QExtendedLabel(self)
		self.modpack_desc.setText(f"Please report ASAP")
		self.modpack_desc.move(250, 475)
		self.modpack_desc.setStyleSheet(h.load_stylesheet(True)["modpack_info"])
		self.modpack_desc.adjustSize()

		self.modpack_desc2 = QExtendedLabel(self)
		self.modpack_desc2.setText(f"am:{self.active_modpack}-noCall?")
		self.modpack_desc2.move(250, 485)
		self.modpack_desc2.setStyleSheet(h.load_stylesheet(True)["modpack_info_small"])
		self.modpack_desc2.adjustSize()

		self.update_playUI_selected_modpack()

		elems.append(self.modpack_title)
		elems.append(self.modpack_desc)
		elems.append(self.modpack_desc2)

		# Play part
		plab = QExtendedLabel(self)
		plab.setText("Play")
		plab.move(210, 50)
		plab.setStyleSheet(h.load_stylesheet(True)["launcher_part_selected"])
		plab.clicked.connect(lambda null=None: self.switch_page("play"))
		elems.append(plab)
		self.buttons.append(plab)

		# Modpack part
		mlab = QExtendedLabel(self)
		mlab.setText("Modpack")
		mlab.move(260, 50)
		mlab.setStyleSheet(h.load_stylesheet(True)["launcher_part"])
		mlab.clicked.connect(lambda null=None: self.switch_page("modpack"))
		elems.append(mlab)
		self.buttons.append(mlab)

		self.pages["play"][1] = elems

	def update_playUI_selected_modpack(self):
		if self.active_modpack == self.modpack_info["latest"]:
			icon = self.furnace_icon
		elif self.active_modpack_info["discourage"]:
			icon = self.sand_icon
		else:
			icon = self.crafting_table_icon

		self.modpack_icn.setPixmap(QPixmap(str(icon)))

		self.modpack_title.setText(f"Modpack v{self.active_modpack_info['sv']}")
		self.modpack_title.adjustSize()

		self.modpack_desc.setText(f"V{self.active_modpack_info['mpv']}-{self.active_modpack_info['loader']}")
		self.modpack_desc.adjustSize()

		self.modpack_desc2.setText(f"fm:{self.active_modpack_info['format']}")
		self.modpack_desc2.adjustSize()

	def modpackUI(self):
		elems = []

		# Play part
		plab = QExtendedLabel(self)
		plab.setText("Play")
		plab.move(210, 50)
		plab.setStyleSheet(h.load_stylesheet(True)["launcher_part"])
		plab.clicked.connect(lambda null=None: self.switch_page("play"))
		elems.append(plab)
		self.buttons.append(plab)

		# Modpack part
		mlab = QExtendedLabel(self)
		mlab.setText("Modpack")
		mlab.move(260, 50)
		mlab.setStyleSheet(h.load_stylesheet(True)["launcher_part_selected"])
		mlab.clicked.connect(lambda null=None: self.switch_page("modpack"))
		elems.append(mlab)
		self.buttons.append(mlab)

		msellab = QExtendedLabel(self)
		msellab.setText("Selected modpack")
		msellab.move(210, 80)
		msellab.setStyleSheet(h.load_stylesheet(True)["modpack_title"])
		msellab.adjustSize()
		elems.append(msellab)

		self.msel = QComboBox(self)
		self.msel.move(210, 100)
		self.msel.currentIndexChanged.connect(self.change_active_modpack)
		self.show_all_checkmark = QCheckBox(self)
		self.show_all_checkmark.move(210, 120)
		self.show_all_checkmark.clicked.connect(self.update_modpackUI_modpacks)
		elems.append(self.show_all_checkmark)
		self.buttons.append(self.show_all_checkmark)

		show_all_checkmark_text = QExtendedLabel(self)
		show_all_checkmark_text.setText("Show all modpacks")
		show_all_checkmark_text.move(230, 127)
		show_all_checkmark_text.adjustSize()
		elems.append(show_all_checkmark_text)

		self.msel.view().window().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
		elems.append(self.msel)
		self.update_modpackUI_modpacks(None)

		self.pages["modpack"][1] = elems

	def change_active_modpack(self):
		if self.msel.currentText() == "":  # If .clear() in update_modpackUI_modpacks()
			return
		selm = self.msel.currentText().split()[0].replace("v", "", 1)
		self.active_modpack = selm
		self.active_modpack_info = self.modpack_info["all"][self.active_modpack]

		self.update_playUI_selected_modpack()

	def update_modpackUI_modpacks(self, e):
		self.msel.clear()

		furnace_icon = QIcon(str(self.furnace_icon))
		crafting_icon = QIcon(str(self.crafting_table_icon))
		sand_icon = QIcon(str(self.sand_icon))
		i = 0
		for item in reversed(self.modpack_info["all"]):
			current = self.modpack_info["all"][item]
			if item == self.modpack_info["latest"]:
				icon = furnace_icon
			elif current["discourage"]:
				icon = sand_icon

				if not self.show_all_checkmark.isChecked():
					i += 1
					continue
			else:
				icon = crafting_icon

			self.msel.addItem(icon, f"v{item} ({current['mpv']}-{current['mcv']}-{current['sv']})")
			if item == self.active_modpack:
				self.msel.setCurrentIndex(i)
			self.msel.adjustSize()
			i += 1

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

		for p in self.pages:
			if len(self.pages[p]) >= 3:
				if p == page:
					self.pages[p][2].setStyleSheet(h.load_stylesheet(True)["launcher_name_selected"])
				else:
					self.pages[p][2].setStyleSheet(h.load_stylesheet(True)["launcher_name"])

	def reload_app(self):
		# Download background image
		h.img_webreq(h.secondary_api_path + "/background.png", "launcher_bg.png")

		self.pages = {
			"play": [self.playUI, []],
			"modpack": [self.modpackUI, []],
			"changelog": [self.changelogUI, []],
			"settings": [self.settingsUI, []]
		}
		self.playUI()
		self.modpackUI()
		self.changelogUI()
		self.settingsUI()

		self.current_page = None
		self.switch_page("play")
		self.switch_page("modpack")
		self.switch_page("changelog")
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
