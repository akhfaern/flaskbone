from flask import Blueprint, request, Response, abort
from os import path
import json
from fb.constants import HOME_DIR
from importlib import import_module
from fb.lib.base_request_class import BaseRequestClass
import inspect

bp = Blueprint('generic', __name__, url_prefix='/')


def get_instance(class_name: str):
    class_path = path.join(HOME_DIR, "lib", f"{class_name}.py")
    if not path.exists(class_path):
        return None, None
    file = import_module(f"fb.lib.{class_name}")
    class_attributes = [attr for attr in dir(file) if attr[0:2] != '__' and attr != 'BaseRequestClass']
    if len(class_attributes) < 1:
        return None, None
    instance = None
    method_names = None
    for class_attribute in class_attributes:
        base_class = getattr(file, class_attribute)
        try:
            if inspect.isclass(base_class) and issubclass(base_class, BaseRequestClass):
                instance = base_class()
                method_names = [attr for attr in dir(instance) if inspect.ismethod(getattr(instance, attr))]
        except TypeError:
            print(base_class, BaseRequestClass)
    return instance, method_names


@bp.route('/<string:class_name>', methods=['GET', 'POST'])
def get_post(class_name: str):
    instance, method_names = get_instance(class_name=class_name)
    if instance is None:
        abort(404)
    result = {}
    if request.method == 'GET' and 'get' in method_names:
        result = instance.get()
    elif request.method == 'POST' and 'post' in method_names:
        json_data = request.get_json()
        result = instance.post(json_data)
    else:
        abort(405)
    result_string = json.dumps(result)
    return Response(result_string, mimetype='application/json')


@bp.route('/<string:class_name>/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete(class_name: str, id: int):
    instance, method_names = get_instance(class_name=class_name)
    if instance is None:
        abort(404)
    result = {}
    if request.method == 'GET' and 'get' in method_names:
        result = instance.get(id)
    elif request.method == 'PUT' and 'put' in method_names:
        json_data = request.get_json()
        result = instance.put(json_data)
    elif request.method == 'DELETE' and 'delete' in method_names:
        result = instance.delete(id)
    else:
        abort(405)
    result_string = json.dumps(result)
    return Response(result_string, mimetype='application/json')
