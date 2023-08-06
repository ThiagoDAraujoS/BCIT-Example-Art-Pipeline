from ShowSafari.show_manager import ShowManager
from ShowSafari.asset_library import AssetLibrary


if __name__ == '__main__':
    path = "C:\\Users\\Thiago\\Desktop\\BCIT-Example-Art-Pipeline\\Examples"

    # Create a Library Instance using a project path
    library = AssetLibrary(path)
    instance = ShowManager(path, library)

    instance.create_show("chickens")
    shot_id = instance.create_shot("chickens", "shot1")
    audio_id = library.create("music", "Audio")
    library.connect(shot_id, audio_id)
