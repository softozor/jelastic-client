class UserInfo:
    """
    Jelastic user info.
    """

    def __init__(self, user_info: dict):
        self._info = user_info

    def email(self) -> str:
        return self._info["email"]
