from App.ShowManager import Manager
import os.path as path

if __name__ == '__main__':
    FOLDER = path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')
    manager = Manager.Manager()
    manager.install(FOLDER)
    manager.create_show("Super Raptors")
