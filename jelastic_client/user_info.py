class UserInfo:
    """
    Jelastic user information.
    """

    def __init__(self, user_info: dict):
        self._info = user_info

    def email(self) -> str:
        return self._info["email"]
