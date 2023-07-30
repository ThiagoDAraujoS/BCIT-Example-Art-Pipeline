from ShowSafari.instance import Instance

if __name__ == '__main__':
    i = Instance("D:\\Library\\Examples")
    i.create_show("chickens")
    shot_id = i.create_shot("chickens", "shot1")
    audio_id = i.library.create("music", "Audio")
    i.library.connect_asset(shot_id, audio_id)
