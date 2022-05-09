import re


class Validator:
    def __init__(self) -> None:
        self.RECORD_NAME_REGEX = "^[a-zA-Z0-9ğüşöçıİĞÜŞÖÇI\\._-]{0,256}$"
        self.URL_REGEX = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}" \
                         r"([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
        self.NUMBER_REGEX = "^[0-9]{0,10}$"
        self.SIZE_REGEX = "^([1-9]|[1][0-9]|2[0])$"
        self.ALLOWDENY_REGEX = "^(allow|deny)$"
        self.NAME_REGEX = "^[a-zA-Z0-9ğüşöçıİĞÜŞÖÇI _-]{0,256}$"
        self.FILE_NAME_REGEX = "^[^\\\\\\/:\\*\\!?`'&$;\"<>\\|]+$"
        self.PASSWORD_REGEX = "^.*$"
        self.EMAIL_REGEX = "^[a-zA-Z0-9.!#$%&'*+\\/=?^_`{|}~-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        self.PORT_REGEX = "^()([0-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$"
        self.IP_REGEX = "^(?:(?:^|\\.)(?:2(?:5[0-5]|[0-4]\\d)|1?\\d?\\d)){4}$"
        self.IP_PORT_REGEX = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
        self.NO_SPECIAL_CHAR_REGEX = "^[a-zA-Z0-9_.()-]{1,48}$"
        self.IP_CIDR = "^([0-9]{1,3}.){3}[0-9]{1,3}($|/(16|24|32))$"

    def test_string(self, test_string: str, pattern: str):
        p = re.compile(self.__dict__.get(pattern), re.IGNORECASE)
        matched = p.match(str(test_string))
        return bool(matched)

    def validate(self, test_string: str, pattern: str) -> bool:
        if pattern.find("#") > -1:
            # we will accept # as or statement
            patterns = pattern.split("#")
            for _pattern in patterns:
                res = self.test_string(test_string=test_string, pattern=_pattern)
                # either any of them is true
                if res is True:
                    return True
            return False
        else:
            return self.test_string(test_string=test_string, pattern=pattern)

    def validate_list(self, testing: list) -> bool:
        for k, v in testing:
            if isinstance(k, str) and k.strip() != '':
                t = self.validate(k, v)
                if not t:
                    return False
            elif isinstance(k, list):
                for b in k:
                    t = self.validate(b, v)
                    if not t:
                        return False
        return True

    def get_pattern(self, pattern: str) -> str:
        return self.__dict__.get(pattern)
