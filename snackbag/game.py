import os
import shutil
import sys
import zipfile

import snackbag.helper as h
from portablemc.standard import Version, Context
from portablemc.fabric import FabricVersion
from portablemc.forge import ForgeVersion
from pathlib import Path
from snackbag.event import call_event, EventListener


def get_name_from_format(name: str, format: str, format_args: dict) -> str:
	if format == "legacy-first":
		return name
	elif format == "lowend-highend":
		if format_args.get("type") is None:
			print("\nError: Invalid format_args\n")
			sys.exit(1)
		n = name.split("-")
		nb = 0
		rv = ""
		for i in n:
			if nb == 1:
				rv += f"{format_args['type']}-"
				nb += 1

			rv += i + "-"
			nb += 1

		if len(n) > 1:
			return rv[:-1]
		else:
			return n[0] + "-" + format_args["type"]


def start_game(modpack_info: dict, format_args: dict = {}):
	runs = Path("snackbag") / Path("runs")
	context = Context(runs / Path(modpack_info["run_folder"]), runs / Path(modpack_info["run_folder"]))

	if modpack_info["hard_loader"] == "vanilla":
		game = Version(modpack_info["loader"], context=context).install()
		call_event(EventListener.GAME_INSTALL_FINISHED_EVENT)
		game.run()
		call_event(EventListener.GAME_STOPPED_EVENT)
	elif modpack_info["hard_loader"] == "fabric":
		fabric_version = FabricVersion.with_fabric(modpack_info["mcv"], modpack_info["loader"].split(":")[2])
		fabric_version.context = context
		game = fabric_version.install()
		call_event(EventListener.GAME_INSTALL_FINISHED_EVENT)
		game.run()
		call_event(EventListener.GAME_STOPPED_EVENT)
	elif modpack_info["hard_loader"] == "forge":
		game = ForgeVersion(modpack_info["loader"].split(":")[1], context=context).install()
		call_event(EventListener.GAME_INSTALL_FINISHED_EVENT)
		game.run()
		call_event(EventListener.GAME_STOPPED_EVENT)
	else:
		print(f"\nError: Invalid hard_loader {modpack_info['hard_loader']}\n")
		sys.exit(1)


def install_modpack(modpack_name: str, instance: str, ignore_cache: bool = False):
	install_path = f"../runs/{instance}/mods/{modpack_name}.zip"
	hard_install_path = Path("snackbag") / Path("runs") / Path(instance) / Path("mods") / Path(f"{modpack_name}.zip")

	if os.path.isfile(hard_install_path.parent / Path("cache.txt")):
		with open(hard_install_path.parent / Path("cache.txt"), "r") as f:
			file = f.readlines()
			if file[0] == modpack_name:
				print("Ignore modpack installation - already cached")
				call_event(EventListener.MODPACK_INSTALL_FINISHED_EVENT)
				return

	try:
		shutil.rmtree(hard_install_path.parent)
	except FileNotFoundError:
		pass

	os.mkdir(hard_install_path.parent)

	h.img_webreq(h.secondary_api_path + f"/../{modpack_name}.zip", install_path)
	with zipfile.ZipFile(hard_install_path, 'r') as zip_ref:
		zip_ref.extractall(hard_install_path.parent)
	os.remove(hard_install_path)

	with open(hard_install_path.parent / Path("cache.txt"), "w") as f:
		f.write(modpack_name)

	call_event(EventListener.MODPACK_INSTALL_FINISHED_EVENT)
