"""
Author: Murat Cem YALIN
https://github.com/akhfaern/pythonDataValidation
License: MIT
"""

from typing import Union

from fb.data_classes.validator import Validator


class BaseDataClass:
    def __init__(self, data: dict) -> None:
        self.__data = data
        self.__validator = Validator()
        self.__validation_errors = {}

    def get_data(self) -> dict:
        class_vars = self.__class__.__dict__
        r_dict = {}
        for v in class_vars:
            if v[0:2] != "__":
                r_dict[v] = self.__data.get(v)
        return r_dict

    def __add_validation_error(self, v: str, error_value: str, v_key: str = None):
        if v_key is not None:
            if v not in self.__validation_errors:
                self.__validation_errors[v] = {}
            self.__validation_errors[v][v_key] = error_value
        else:
            self.__validation_errors[v] = error_value

    @staticmethod
    def __check_is_required(validation_rule: Union[str, tuple]):
        if type(validation_rule) is not tuple:
            return validation_rule, "NOTREQUIRED"
        return validation_rule

    def __check_required_condition(self, required_condition: str) -> bool:
        if required_condition[0:10] == "REQUIREDIF":
            required = required_condition.split("_")
            value = self.__data.get(required[1].replace("-", "_"))
            condition = required[2]
            equation = required[3]
            if equation.lower() == 'true':
                equation = True
            elif equation.lower() == 'false':
                equation = False
            if condition == 'is':
                return value == equation
            if condition == 'in':
                return value in equation.split(',')
        return False

    def __validate_list(self, v: str, value: dict, validation_rules: Union[list, tuple]) -> bool:
        validation_rules, is_required = BaseDataClass.__check_is_required(validation_rule=validation_rules)
        if (is_required == "REQUIRED" or self.__check_required_condition(is_required)) and len(value) == 0:
            self.__add_validation_error(v, "Value is required", "[]")
            return False
        if isinstance(validation_rules[0], dict):
            for list_val in value:
                self.__validate_dict(v=v, value=list_val, validation_rules=validation_rules[0])
        elif isinstance(validation_rules[0], list):
            val_type = validation_rules[0][0]
            validation_rule = validation_rules[0][1]
            for list_val in value:
                if val_type == 'str':
                    self.__validate_str(v=v, value=list_val, validation_rule=validation_rule)
                if val_type == 'int':
                    self.__validate_int(v=v, value=list_val, validation_rule=validation_rule)
        else:
            if v not in self.__validation_errors:
                self.__validation_errors[v] = {}
            self.__validation_errors[v][validation_rules[0]] = 'unknown type'
        return True

    def __validate_dict(self, v: str, value: dict, validation_rules: Union[dict, tuple]) -> bool:
        validation_rules, is_required = BaseDataClass.__check_is_required(validation_rule=validation_rules)
        if len(value) != len(validation_rules):
            self.__validation_errors[v] = 'length error'
            return False
        for key in validation_rules:
            v_value = value.get(key, None)
            if v_value is None:
                self.__add_validation_error(v, "Value required", key)
            return self.__validate_str(v, str(v_value), validation_rule=validation_rules[key], v_key=key)
        return True

    def __validate_str(self, v: str, value: str, validation_rule: Union[str, tuple], v_key: str = None) -> bool:
        validation_rule, is_required = BaseDataClass.__check_is_required(validation_rule=validation_rule)
        if (is_required == "REQUIRED" or self.__check_required_condition(is_required)) and (str(value).strip() == "" or
                                                                                            value is None):
            self.__add_validation_error(v, "Value is required", v_key)
            return False
        if value is not None and str(value).strip() != "" and not self.__validator.validate(str(value),
                                                                                            validation_rule):
            self.__add_validation_error(v, value, v_key)
            return False
        return True

    def __validate_int(self, v: str, value: int, validation_rule: Union[str, tuple], v_key: str = None) -> bool:
        validation_rule, is_required = BaseDataClass.__check_is_required(validation_rule=validation_rule)
        if is_required == "REQUIRED" and type(value) is not int:
            self.__add_validation_error(v, str(value), v_key)
            return False
        if value is not None:
            if type(validation_rule) is int and type(value) is not int:
                self.__add_validation_error(v, str(value), v_key)
                return False
            if type(validation_rule) is str:
                _validation_rule = validation_rule.split("_")
                if _validation_rule[0] == "NUMBERBETWEEN":
                    min_value = int(_validation_rule[1])
                    max_value = int(_validation_rule[2])
                    if value < min_value or value > max_value:
                        self.__add_validation_error(v, str(value), v_key)
                        return False
                elif not self.__validator.validate(str(value), validation_rule):
                    self.__add_validation_error(v, str(value), v_key)
                    return False
        return True

    def __validate_bool(self, v: str, value: bool, validation_rule: Union[str, tuple], v_key: str = None) -> bool:
        validation_rule, is_required = BaseDataClass.__check_is_required(validation_rule=validation_rule)
        if is_required == "REQUIRED" and type(value) is not bool:
            self.__add_validation_error(v, str(value), v_key)
            return False
        if value is not None and type(value) is not bool:
            self.__add_validation_error(v, str(value), v_key)
            return False
        return True

    def __validate_data(self) -> None:
        self.__validation_errors = {}
        class_vars = self.__class__.__dict__
        annotations = class_vars.get('__annotations__', None)
        for v in class_vars:
            if v[0:2] != "__":
                value = self.__data.get(v)
                validation = class_vars[v]
                annotation = annotations[v]
                if value is not None and not isinstance(value, annotation):
                    self.__validation_errors[v] = value
                elif annotation is str:
                    self.__validate_str(v=v, value=value, validation_rule=validation)
                elif annotation is int:
                    self.__validate_int(v=v, value=value, validation_rule=validation)
                elif annotation is bool:
                    self.__validate_bool(v=v, value=value, validation_rule=validation)
                elif annotation is dict:
                    self.__validate_dict(v=v, value=value, validation_rules=validation)
                elif annotation is list:
                    self.__validate_list(v=v, value=value, validation_rules=validation)

    def is_validated(self) -> bool:
        self.__validate_data()
        return len(self.__validation_errors) == 0

    def get_validation_errors(self) -> dict:
        return self.__validation_errors
