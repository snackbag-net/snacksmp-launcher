import enum


class EventInfo:
	functions = {}


class EventListener(enum.Enum):
	GAME_INSTALL_FINISHED_EVENT = 1
	MODPACK_INSTALL_FINISHED_EVENT = 2
	MODPACK_DOWNLOAD_FINISHED_EVENT = 4
	GAME_STOPPED_EVENT = 3


def call_event(event: EventListener, args: dict = {}):
	if EventInfo.functions.get(event) is None:
		return

	for func in EventInfo.functions[event]:
		func(args)


def register_event(event: EventListener, function):
	if EventInfo.functions.get(event) is None:
		EventInfo.functions[event] = []
	EventInfo.functions[event].append(function)
