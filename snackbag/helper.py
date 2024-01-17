import json
from pathlib import Path
import urllib.request
from PIL import Image
from io import BytesIO

api_path = "https://extras.snackbag.net/api/launcher_api"
secondary_api_path = "https://snackbag.net/extras/snacksmp/launcher"
ctx = None


def load_stylesheet(extra: bool = False):
	if extra:
		return json.load(open(Path("snackbag") / Path("storage") / Path("theme.css.json")))
	return open(Path("snackbag") / Path("storage") / Path("theme.css")).read()


def img_webreq(url: str, save_as: str):
	urllib.request.urlretrieve(url, Path("snackbag") / Path("storage") / Path(save_as))


def webreq(url: str):
	return urllib.request.urlopen(url).read()
