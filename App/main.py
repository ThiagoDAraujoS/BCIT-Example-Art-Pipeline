from App.ShowManager.Proxy import *

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")


#
#from App.ShowManager import Manager, Show
#import os.path as path
#
#
#if __name__ == '__main__':
#    FOLDER = path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')
#    manager = Manager.Manager()
#    manager.install(FOLDER)
#    manager.create_element("Super Raptors")
#    manager = Manager.Manager()
#    manager.load_folder(FOLDER)
#
