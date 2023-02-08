import ast
import os
from typing import List

from models import ClassData, Field, Method
from pyignore import IGNORED_FOLDERS
from env import DIRECTORY


FIELD_TYPES = [
    "models.ForeignKey",
    "models.CharField",
    "models.TextField",
    "models.IntegerField",
    "models.FloatField",
    "models.BooleanField",
    "models.DateField",
    "models.DateTimeField",
    "models.TimeField",
]


def extract_field_params(field_node):
    if isinstance(field_node.value, ast.Constant):
        #print('Field Node Value: ', field_node.arg, field_node.value.value)
        param_name = field_node.arg
        param_value = field_node.value.value
        #print(f"{param_name}: {param_value}")
        return param_name, param_value


def extract_field(node):
    field = {}
    value = node.value
    if not isinstance(value, ast.Call):
        return None

    field["name"] = node.targets[0].id
    field["type"] = value.func.attr
    field["params"] = []

    if len(value.args) > 0 and len(value.keywords) > 0:
        arg = value.args[0]
        params = []
        for keyword in value.keywords:
            params.append(extract_field_params(keyword))

        # Fields (TextField, CharField, DecimalField, etc.)
        if isinstance(arg, ast.Call):
            sub_arg = arg.args[0]
            if isinstance(sub_arg, ast.Call):
                name = sub_arg.args[0].value
                field["name"] = name
                field["params"] = params
            elif isinstance(sub_arg, ast.Constant):
                name = sub_arg.value
                field["name"] = name
                field["params"] = params
        # Relational Fields
        elif isinstance(arg, ast.Name):
            name = arg.id
            field["related_model"] = name
            field["params"] = params
        elif isinstance(arg, ast.Constant):
            name = arg.value
            field["related_model"] = name
            field["params"] = params
    return field


def extract_method(body_node):
    return Method(body_node.name,[a.arg for a in body_node.args.args],)


def extract_class_data(code):
    module = ast.parse(code)
    class_data = []
    for node in module.body:
        if is_class(node):
            name = node.name
            fields = []
            methods = []
            for node in node.body:
                if is_method(node):
                    extracted_method = extract_method(node)
                    methods.append(extracted_method)
                elif is_field(node):
                    extracted_field = extract_field(node)
                    fields.append(extracted_field)

            class_data.append(ClassData(name, fields, methods))
            print(class_data)
    return class_data


def is_field(node):
    if not isinstance(node, ast.Assign):
        return False
    value = node.value
    if (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Attribute)
            and value.func.value.id == "models"
    ):
        return True
    return False


def is_class(node):
    return isinstance(node, ast.ClassDef)


def is_attribute(node):
    return isinstance(node, ast.Attribute)


def is_method(node):
    return isinstance(node, ast.FunctionDef)


def extract_from_folder() -> dict[str, List[ClassData]]:
    all_class_data = {}

    data_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", DIRECTORY)
    )

    for root, dirs, files in os.walk(data_folder):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
        if "models.py" not in files:
            continue
        if "__init__.py" not in files:
            continue
        models_file = os.path.join(root, "models.py")
        if os.path.exists(models_file) and os.path.isfile(models_file):
            with open(models_file, "r") as f:
                source = f.read()
                class_data = extract_class_data(source)
        else:
            print(
                f"Error: file '{models_file}' doesn't exist or is unreadable"
            )
        if len(class_data) == 0:
            continue
        all_class_data[os.path.basename(root)] = class_data
    return all_class_data
