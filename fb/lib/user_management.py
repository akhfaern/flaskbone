from fb.lib.base_request_class import BaseRequestClass
from fb.lib.config import Config
from fb.data_classes.user_data import UserData
import copy
import jwt
import json


class UserManagement(BaseRequestClass):
    def __init__(self) -> None:
        super().__init__()
        self.config_manager = Config(dir_path="configs/", config_name="users.json")
        self.logger = self.config_manager.logger

    def get(self) -> list:
        config = copy.deepcopy(self.config_manager.config)
        for c in config:
            c["password"] = ""
        return config

    def get_user_by_username_with_password(self, username: str) -> [dict, None]:
        return self.config_manager.get_config_by_field('username', username)

    def get_user_by_refresh_token(self, refresh_token: str) -> [dict, None]:
        return self.config_manager.get_config_by_field('refreshToken', refresh_token)

    @staticmethod
    def decode(auth):
        return jwt.decode(auth, "secret_code", algorithms=["HS256"])

    @staticmethod
    def encode(user):
        return jwt.encode(user, "secret_code", algorithm="HS256")

    def post(self, data: dict) -> dict:
        try:
            user_data = UserData(data)
            if user_data.is_validated():
                self.logger.info("User added: {0}".format(data.get('username')))
                return self.config_manager.add(user_data.get_data())
            else:
                self.logger.info("User validation error: {0}".format(json.dumps(user_data.get_validation_errors())))
                return {"result": False, "error": f"user validation error: {user_data.get_validation_errors()}"}
        except Exception as e:
            self.logger.error("User add error: {0}".format(e))
        return {"result": False}

    def put(self, user_id: int, data: dict) -> dict:
        try:
            password = data.get('password', '').strip()
            if len(password) == 0:
                user = self.config_manager.get(int(data.get('id', 0)))
                data["password"] = user.get('password')
            if user_id == 1:
                data["active"] = True
            user_data = UserData(data)
            if user_data.is_validated():
                self.logger.info("User edited: {0}".format(data.get('username')))
                return self.config_manager.edit(user_id, user_data.get_data())
            else:
                self.logger.info("User validation error: {0}".format(json.dumps(user_data.get_validation_errors())))
                return {"result": False, "error": f"user validation error: {user_data.get_validation_errors()}"}
        except Exception as e:
            self.logger.error("DNS add error: {0}".format(e))
        return {"result": False}

    def delete(self, user_id: int) -> dict:
        if user_id == 1:
            return {"result": False, "error": "First user can not be deleted"}
        user = self.config_manager.get_config_by_id(user_id)
        if user is not None:
            self.logger.info("User deleted: {0}".format(user.get('username')))
            return self.config_manager.delete(user_id)
        return {"result": False, "error": "User not found"}
