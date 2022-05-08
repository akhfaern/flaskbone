from fb.data_classes.base_data_class import BaseDataClass


class UserData(BaseDataClass):
    username: str = ("NAME_REGEX", "REQUIRED")
    password: str = "PASSWORD_REGEX"
    fullname: str = ("FULL_NAME_REGEX", "REQUIRED")
    active: bool = (False, "REQUIRED")
