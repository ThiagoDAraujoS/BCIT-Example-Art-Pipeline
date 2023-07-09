from App.ShowManager import Manager, Show
import os.path as path

if __name__ == '__main__':
    FOLDER = path.normpath('C://Users//Thiago//Desktop//Bcit Projects//Pipeline//Example')
    manager = Manager.Manager(FOLDER)
    manager.build()
    manager.create_element("Super Raptors")
    manager = Manager.Manager(FOLDER)
    manager.load_from_folder()
