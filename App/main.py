from App.ShowManager import Manager, Show
import os.path as path

if __name__ == '__main__':
    FOLDER = path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')
    manager = Manager.Manager()
    manager.install(FOLDER)
    manager.create_element("Super Raptors")
    manager = Manager.Manager()
    manager.load_folder(FOLDER)
    manager.print_names()
