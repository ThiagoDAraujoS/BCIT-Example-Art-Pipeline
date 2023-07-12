from .Manager import Manager
from .Serializable.Serializable import BuildExitCode

manager = Manager()


def install(folder: str) -> int:
    manager.set_folder(folder)
    exit_code = manager.build()
    if exit_code == BuildExitCode.SUCCESS:
        print("Installed Successfully")
    elif exit_code == BuildExitCode.FOLDER_COLLISION:
        print("Folder path not empty")
    elif exit_code == BuildExitCode.PROJECT_OVERRIDE:
        print("A project already exists in folder path")
    else:
        print("An error has occurred")
    return exit_code.value


def load(folder: str) -> None:
    manager.set_folder(folder)
    manager.load_from_folder()
    print(f"Project at {folder} loaded successfully")


def get_shows_list() -> list[str]:
    show_list = manager.get_names()
    print(f"This are the saved shows, ", show_list)
    return show_list


def create_show(show_name: str) -> None:
    manager.create_element(show_name)


def delete_show(show_name: str) -> None:
    manager.delete(show_name)


def get_show_data(show_name: str) -> dict[str, object]:
    return manager[show_name]


def set_show_data(show_name: str, data: dict[str, object]):
    manager[show_name].__dict__.update(data)
    manager[show_name].serialize()


def get_shot_list(show_name):
    shot_list = manager[show_name].get_names()
    print(shot_list)
    return shot_list


def create_shot(show_name: str, shot_name: str):
    manager[show_name].create_element(shot_name)


def get_shot_data(show_name, shot_name):
    return manager[show_name][shot_name]


def delete_shot(show_name, shot_name):
    manager[show_name].delete(shot_name)


def set_shot_data(show_name, shot_name, data: str):
    manager[show_name][shot_name].__dict__.update(data)
    manager[show_name][shot_name].serialize()
