from typing import Optional

from nonebot.exception import (AdapterException, ActionFailed as
                               BaseActionFailed, NetworkError as
                               BaseNetworkError, ApiNotAvailable as
                               BaseApiNotAvailable)


class GOCQAdapterException(AdapterException):

    def __init__(self):
        super().__init__("cqhttp")


class ActionFailed(BaseActionFailed, GOCQAdapterException):
    """
    :说明:

      API 请求返回错误信息。

    :参数:

      * ``retcode: Optional[int]``: 错误码
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.info = kwargs

    def __repr__(self):
        return f"<ActionFailed " + ", ".join(
            f"{k}={v}" for k, v in self.info.items()) + ">"

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, GOCQAdapterException):
    """
    :说明:

      网络错误。

    :参数:

      * ``retcode: Optional[int]``: 错误码
    """

    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, GOCQAdapterException):
    pass
