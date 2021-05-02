from typing import Optional

from pydantic import Field, BaseModel


# priority: alias > origin
class Config(BaseModel):
    """
    go-cqhttp 配置类

    :配置项:

      - ``access_token`` / ``cqhttp_access_token``: go-cqhttp 协议授权令牌
      - ``secret`` / ``cqhttp_secret``: go-cqhttp HTTP 上报数据签名口令
    """
    access_token: Optional[str] = Field(default=None,
                                        alias="cqhttp_access_token")
    secret: Optional[str] = Field(default=None, alias="cqhttp_secret")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
