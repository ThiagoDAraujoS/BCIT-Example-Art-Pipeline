from flask import request, jsonify
from ..app import *


@app.route('/')
def test():
    return "hello world"


@app.route('/install', methods=['POST'])
def install():
    """ TODO: ENSURE TO PASS THE CALLBACKS TO TREAT THINGS BREAKING """
    data = request.get_json()
    folder = data.get('folder')
    manager.install(folder)
    return jsonify(message='Application installed successfully'), 200


@app.route('/load', methods=['POST'])
def load():
    """ TODO: ENSURE TO PASS THE CALLBACKS TO TREAT THINGS BREAKING """
    data = request.get_json()
    folder = data.get('folder')
    manager.load_folder(folder)
    return jsonify(message='Application loaded successfully'), 200


@app.route('/shows', methods=['GET'])
def get_show_list():
    """ TODO: TREAT SHOW_NAME NOT EXISTING CATCH"""
    show_name_list = manager.get_names()
    return jsonify(show_name_list), 200


@app.route('/shows', methods=['POST'])
def create_show():
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
    data = request.get_json()
    json = data.get("data")
    manager[show_name].decode(json)
    return jsonify(message='Show data updated successfully'), 200


@app.route('/shows/<show_name>/shots', methods=['GET'])
def get_shot_list(show_name):
    shot_list = manager[show_name].get_names()
    return jsonify(shot_list), 200


@app.route('/shows/<show_name>/shots', methods=['POST'])
def create_shot(show_name):
    data = request.get_json()
    name = data.get("name")
    manager[show_name].create_element(name)
    return jsonify(message='Shot created successfully'), 201


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['GET'])
def get_shot_data(show_name, shot_name):
    shot_data = manager[show_name][shot_name].encode()
    return jsonify(shot_data), 200


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['DELETE'])
def delete_shot(show_name, shot_name):
    manager[show_name].delete(shot_name)
    return jsonify(message='Shot deleted successfully'), 200


@app.route('/shows/<show_name>/shots/<shot_name>', methods=['PUT'])
def set_shot_data(show_name, shot_name):
    data = request.get_json()
    json = data.get("data")
    manager[show_name][shot_name].decode(json)
    return jsonify(message='Shot data updated successfully'), 200
