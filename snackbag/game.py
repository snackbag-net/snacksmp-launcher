import sys

from portablemc.standard import Version, Context
from portablemc.fabric import FabricVersion
from portablemc.forge import ForgeVersion
from pathlib import Path


def start_game(modpack_info: dict):
	runs = Path("snackbag") / Path("runs")
	context = Context(runs / Path(modpack_info["run_folder"]), runs / Path(modpack_info["run_folder"]))

	if modpack_info["hard_loader"] == "vanilla":
		Version(modpack_info["loader"], context=context).install().run()
	elif modpack_info["hard_loader"] == "fabric":
		fabric_version = FabricVersion.with_fabric(modpack_info["mcv"], modpack_info["loader"].split(":")[2])
		fabric_version.context = context
		fabric_version.install().run()
	elif modpack_info["hard_loader"] == "forge":
		ForgeVersion(modpack_info["loader"].split(":")[1], context=context).install().run()
	else:
		print(f"\nError: Invalid hard_loader {modpack_info['hard_loader']}\n")
		sys.exit(1)
