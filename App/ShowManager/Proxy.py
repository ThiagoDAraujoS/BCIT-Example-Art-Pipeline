from flask import request, jsonify
from ..app import *
from App.ShowManager.Serializable.Serializable import BuildExitCode


@app.route('/')
def test():
    return "hello world"


# ---------------------------PROJECT CALLS-----------------------------------


@app.route('/project', methods=['GET'])
def get_project_names():
    projects = manager.deserialize_bookkeeper()
    return projects, 200


@app.route('/build', methods=['POST'])
def build_new_project():
    data = request.get_json()
    name = data.get("name")
    folder = data.get('folder')

    exit_code = manager.build(name, folder)

    match exit_code:
        case BuildExitCode.SUCCESS:
            return jsonify(message='Project built successfully!'), 200
        case BuildExitCode.FOLDER_COLLISION:
            return jsonify(message='Folder already exists on folder path location.'), 400
        case BuildExitCode.PATH_BROKEN:
            return jsonify(message='Folder path illegal.'), 401
        case BuildExitCode.PROJECT_OVERRIDE:
            return jsonify(message='Older project located on folder path.'), 402
        case _:
            return jsonify(message='An Error has occurred.'), 500


@app.route('/project', methods=['POST'])
def load_project():
    """ TODO: ENSURE TO PASS THE CALLBACKS TO TREAT THINGS BREAKING """
    data = request.get_json()
    folder = data.get('name')

    book = manager.deserialize_bookkeeper()
    manager.set_folder(book[folder])
    manager.load_from_folder()

    show_name_list = manager.get_names()
    return jsonify(show_name_list), 200


@app.route('/project', methods=['DELETE'])
def delete_project():
    data = request.get_json()
    name = data.get('name')
    manager.delete_project(name)


# ---------------------------SHOW CALLS-----------------------------------


@app.route('/shows', methods=['GET'])
def get_show_names():
    """ TODO: TREAT SHOW_NAME NOT EXISTING CATCH"""
    show_name_list = manager.get_names()
    return jsonify(show_name_list), 200


@app.route('/shows', methods=['POST'])
def create_new_show():
    """ TODO: IMPLEMENT ON ELEMENT EXIST CATCH """
    data = request.get_json()
    name = data.get("name")
    manager.create_element(name)
    return jsonify(message='Show created successfully'), 201


@app.route('/shows/<show_name>', methods=['DELETE'])
def delete_show(show_name):
    manager.delete(show_name)
    return jsonify(message='Shot deleted successfully'), 200


@app.route('/shows/<show_name>', methods=['GET'])
def get_show_data(show_name):
    """ TODO: TREAT SHOW_NAME NOT EXISTING CATCH"""
    show_data = manager[show_name].encode()
    return show_data, 200


@app.route('/shows/<show_name>', methods=['PUT'])
def set_show_data(show_name):
    data = request.data.decode('utf-8')
    manager[show_name].decode(data)
    manager[show_name].serialize()
    return jsonify(message='Show data updated successfully'), 200


# ---------------------------SHOT CALLS-----------------------------------


@app.route('/shows/<show_name>/shots', methods=['GET'])
def get_shot_names(show_name):
    shot_list = manager[show_name].get_names()
    return jsonify(shot_list), 200


@app.route('/shows/<show_name>/shots', methods=['POST'])
def create_new_shot(show_name):
    data = request.get_json()
    name = data.get("name")
    manager[show_name].create_element(name)
    return jsonify(message='Shot created successfully'), 201


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['GET'])
def get_shot_data(show_name, shot_name):
    shot_data = manager[show_name][shot_name].encode()
    return shot_data, 200


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['DELETE'])
def delete_shot(show_name, shot_name):
    manager[show_name].delete(shot_name)
    return jsonify(message='Shot deleted successfully'), 200


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['PUT'])
def set_shot_data(show_name, shot_name):
    data = request.data.decode('utf-8')
    manager[show_name][shot_name].decode(data)
    manager[show_name][shot_name].serialize()
    return jsonify(message='Show data updated successfully'), 200
