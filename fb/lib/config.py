import json
from os.path import join
from fb.lib.logger import FlaskBoneLogger
from fb.constants import HOME_DIR


class Config:
    def __init__(self, dir_path: str, config_name: str) -> None:
        self.config = []
        self.config_file = join(HOME_DIR, dir_path, config_name)
        self.logger = FlaskBoneLogger.get_logger(name="flaskbone")
        self.load_config()

    def load_config(self) -> None:
        try:
            with open(self.config_file) as json_file:
                self.config = json.load(json_file)
        except FileNotFoundError as e:
            self.logger.error(f"Error while reading file. Error: {e}")

    def get_config_by_field(self, field_name: str, field_value: [str, int]) -> [None, str]:
        for c in self.config:
            if c.get(field_name) == field_value:
                return c
        return None

    def get_config_by_id(self, config_id: int) -> [None, str]:
        return self.get_config_by_field(field_name="id", field_value=config_id)

    def write_config(self) -> bool:
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error while writing file. Error: {e}")
        return False

    def get_list(self) -> list:
        return self.config

    def get_next_id(self) -> int:
        current_id = 0
        for c in self.config:
            if int(c.get("id")) > current_id:
                current_id = int(c.get("id"))
        current_id += 1
        return current_id

    def get(self, config_id: int) -> dict:
        config = self.get_config_by_id(config_id)
        if config is not None:
            return config
        return {}

    def add(self, data: dict) -> dict:
        next_id = self.get_next_id()
        data["id"] = next_id
        self.config.append(data)
        result = self.write_config()
        return {"result": result}

    def edit(self, config_id: int, data: dict) -> dict:
        c = self.get_config_by_id(config_id)
        if c is not None:
            c.update(data)
            result = self.write_config()
            return {"result": result}
        return {"result": False}

    def delete(self, config_id) -> dict:
        c = self.get_config_by_id(config_id)
        if c is not None:
            self.config.remove(c)
            result = self.write_config()
            return {"result": result}
        return {"result": False}
