import inspect
from typing_extensions import Literal
from typing import Type, List, Optional, TYPE_CHECKING

from pydantic import BaseModel
from pygtrie import StringTrie
from nonebot import get_bots
from nonebot.utils import escape_tag
from nonebot.typing import overrides
from nonebot.exception import NoLogException
from nonebot.adapters import Event as BaseEvent

from .message import Message

if TYPE_CHECKING:
    from .bot import Bot


class Event(BaseEvent):
    """
    go-cqhttp 协议事件，字段与 go-cqhttp 一致。各事件字段参考 https://docs.go-cqhttp.org/
    """
    __event__ = ""
    time: int
    self_id: int
    post_type: str

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "message_sent", "notice", "request", "meta_event"]:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        return self.post_type

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return str(self.dict())

    @overrides(BaseEvent)
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return False


# Models
class Sender(BaseModel):
    user_id: Optional[int] = None
    nickname: Optional[str] = None
    card: Optional[str] = None
    sex: Optional[Literal["male", "female", "unknown"]] = None
    age: Optional[int] = None
    area: Optional[str] = None
    level: Optional[str] = None
    role: Optional[Literal["owner", "admin", "member"]] = None
    title: Optional[str] = None

    class Config:
        extra = "allow"


class Reply(BaseModel):
    time: int
    message_type: str
    message_id: int
    real_id: int
    sender: Sender
    message: Message

    class Config:
        extra = "allow"


class Anonymous(BaseModel):
    id: int
    name: str
    flag: str

    class Config:
        extra = "allow"


class File(BaseModel):
    id: str
    name: str
    size: int
    busid: int
    url: str

    class Config:
        extra = "allow"

class Device(BaseModel):
    app_id: int
    device_name: str
    device_kind: str

    class Config:
        extra = "allow"

class Status(BaseModel):
    online: bool
    good: bool

    class Config:
        extra = "allow"


# Message Events
class MessageEvent(Event):
    """消息事件"""
    __event__ = "message"
    post_type: Literal["message"]
    message_type: str
    sub_type: str
    message_id: int
    user_id: int
    message: Message
    raw_message: str
    font: int
    sender: Sender
    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """
    reply: Optional[Reply] = None
    """
    :说明: 消息中提取的回复消息，内容为 ``get_msg`` API 返回结果

    :类型: ``Optional[Reply]``
    """

    @overrides(Event)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.message_type}" + (f".{sub_type}"
                                                          if sub_type else "")

    @overrides(Event)
    def get_message(self) -> Message:
        return self.message

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.message.extract_plain_text()

    @overrides(Event)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(Event)
    def get_session_id(self) -> str:
        return str(self.user_id)

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.to_me


class PrivateMessageEvent(MessageEvent):
    """私聊消息"""
    __event__ = "message.private"
    message_type: Literal["private"]
    sub_type: Literal["friend", "group", "group_selg", "other"]
    temp_source: Optional[int] = None
    """
    :说明: 临时会话来源

    :类型: ``int``
    """

    @overrides(Event)
    def get_event_description(self) -> str:
        return (f'Message {self.message_id} from {self.user_id} "' + "".join(
            map(
                lambda x: escape_tag(str(x))
                if x.is_text() else f"<le>{escape_tag(str(x))}</le>",
                self.message)) + '"')


class GroupMessageEvent(MessageEvent):
    """群消息"""
    __event__ = "message.group"
    message_type: Literal["group"]
    sub_type: Literal["normal", "anonymous", "notice"]
    group_id: int
    anonymous: Optional[Anonymous] = None

    @overrides(Event)
    def get_event_description(self) -> str:
        return (
            f'Message {self.message_id} from {self.user_id}@[群:{self.group_id}] "'
            + "".join(
                map(
                    lambda x: escape_tag(str(x))
                    if x.is_text() else f"<le>{escape_tag(str(x))}</le>",
                    self.message)) + '"')

    @overrides(MessageEvent)
    def get_session_id(self) -> str:
        return f"group_{self.group_id}_{self.user_id}"


# MessageSent Events
class MessageSentEvent(MessageEvent):
    """自身消息事件"""
    __event__ = "message_sent"
    post_type: Literal["message_sent"]


class PrivateMessageSentEvent(PrivateMessageEvent):
    """自身私聊消息"""
    __event__ = "message_sent.private"


class GroupMessageSentEvent(GroupMessageEvent):
    """自身群消息"""
    __event__ = "message_sent.group"


# Notice Events
class NoticeEvent(Event):
    """通知事件"""
    __event__ = "notice"
    post_type: Literal["notice"]
    notice_type: str

    @overrides(Event)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.notice_type}" + (f".{sub_type}"
                                                         if sub_type else "")


class GroupUploadNoticeEvent(NoticeEvent):
    """群文件上传事件"""
    __event__ = "notice.group_upload"
    notice_type: Literal["group_upload"]
    group_id: int
    user_id: int
    file: File

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class GroupAdminNoticeEvent(NoticeEvent):
    """群管理员变动"""
    __event__ = "notice.group_admin"
    notice_type: Literal["group_admin"]
    sub_type: Literal["set", "unset"]
    group_id: int
    user_id: int

    @overrides(NoticeEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class GroupDecreaseNoticeEvent(NoticeEvent):
    """群成员减少事件"""
    __event__ = "notice.group_decrease"
    notice_type: Literal["group_decrease"]
    sub_type: Literal["leave", "kick", "kick_me"]
    group_id: int
    operator_id: int
    user_id: int

    @overrides(NoticeEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class GroupIncreaseNoticeEvent(NoticeEvent):
    """群成员增加事件"""
    __event__ = "notice.group_increase"
    notice_type: Literal["group_increase"]
    sub_type: Literal["approve", "invite"]
    group_id: int
    operator_id: int
    user_id: int

    @overrides(NoticeEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class GroupBanNoticeEvent(NoticeEvent):
    """群禁言事件"""
    __event__ = "notice.group_ban"
    notice_type: Literal["group_ban"]
    sub_type: Literal["ban", "lift_ban"]
    group_id: int
    operator_id: int
    user_id: int
    duration: int

    @overrides(NoticeEvent)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class FriendAddNoticeEvent(NoticeEvent):
    """好友添加事件"""
    __event__ = "notice.friend_add"
    notice_type: Literal["friend_add"]
    user_id: int

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class GroupRecallNoticeEvent(NoticeEvent):
    """群消息撤回事件"""
    __event__ = "notice.group_recall"
    notice_type: Literal["group_recall"]
    group_id: int
    user_id: int
    operator_id: int
    message_id: int

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class FriendRecallNoticeEvent(NoticeEvent):
    """好友消息撤回事件"""
    __event__ = "notice.friend_recall"
    notice_type: Literal["friend_recall"]
    user_id: int
    message_id: int

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class NotifyEvent(NoticeEvent):
    """提醒事件"""
    __event__ = "notice.notify"
    notice_type: Literal["notify"]
    sub_type: str
    user_id: int

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class FriendPokeNotifyEvent(NotifyEvent):
    """好友戳一戳提醒事件"""
    __event__ = "notice.notify.poke"
    sub_type: Literal["poke"]
    sender_id: int
    target_id: int

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.target_id == self.self_id


class GroupPokeNotifyEvent(NotifyEvent):
    """群内戳一戳提醒事件"""
    __event__ = "notice.notify.poke"
    sub_type: Literal["poke"]
    group_id: int
    target_id: int

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.target_id == self.self_id


class LuckyKingNotifyEvent(NotifyEvent):
    """群红包运气王提醒事件"""
    __event__ = "notice.notify.lucky_king"
    sub_type: Literal["lucky_king"]
    group_id: int
    target_id: int

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.target_id == self.self_id

    @overrides(NotifyEvent)
    def get_user_id(self) -> str:
        return str(self.target_id)

    @overrides(NotifyEvent)
    def get_session_id(self) -> str:
        return str(self.target_id)


class HonorNotifyEvent(NotifyEvent):
    """群荣誉变更提醒事件"""
    __event__ = "notice.notify.honor"
    sub_type: Literal["honor"]
    group_id: int
    honor_type: Literal["talkative:龙王", "performer:群聊之火", "emotion:快乐源泉"]

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.user_id == self.self_id


class GroupCardNoticeEvent(NoticeEvent):
    """群成员名片更新事件"""
    __event__ = "notice.group_card"
    notice_type: Literal["group_card"]
    group_id: int
    user_id: int
    card_new: str
    card_old: str

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class OfflineFileNoticeEvent(NoticeEvent):
    """接收到离线文件事件"""
    __event__ = "notice.offline_file"
    notice_type: Literal["offline_file"]
    user_id: int
    file: File

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)


class ClientStatusNoticeEvent(NoticeEvent):
    """其他客户端在线状态变更事件"""
    __event__ = "notice.client_status"
    notice_type: Literal["client_status"]
    client: Device
    online: bool


class EssenceMessageNoticeEvent(NoticeEvent):
    """精华消息事件"""
    __event__ = "notice.essence"
    notice_type: Literal["essence"]
    sub_type: Literal["add", "delete"]
    sender_id: int
    operator_id: int
    message_id :int


# Request Events
class RequestEvent(Event):
    """请求事件"""
    __event__ = "request"
    post_type: Literal["request"]
    request_type: str

    @overrides(Event)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.request_type}" + (f".{sub_type}"
                                                          if sub_type else "")


class FriendRequestEvent(RequestEvent):
    """加好友请求事件"""
    __event__ = "request.friend"
    request_type: Literal["friend"]
    user_id: int
    comment: str
    flag: str

    @overrides(RequestEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(RequestEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)

    async def approve(self, remark: str = ""):
        return await get_bots()[self.self_id].set_friend_add_request(flag=self.flag,
                                                                     approve=True,
                                                                     remark=remark)

    async def reject(self):
        return await get_bots()[self.self_id].set_friend_add_request(flag=self.flag, approve=False)


class GroupRequestEvent(RequestEvent):
    """加群请求/邀请事件"""
    __event__ = "request.group"
    request_type: Literal["group"]
    sub_type: Literal["add", "invite"]
    group_id: int
    user_id: int
    comment: str
    flag: str

    @overrides(RequestEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(RequestEvent)
    def get_session_id(self) -> str:
        return str(self.user_id)

    async def approve(self):
        return await get_bots()[self.self_id].set_group_add_request(flag=self.flag,
                                                                    sub_type=self.sub_type,
                                                                    approve=True)

    async def reject(self, reason: str = ""):
        return await get_bots()[self.self_id].set_group_add_request(flag=self.flag,
                                                                    sub_type=self.sub_type,
                                                                    approve=False,
                                                                    reason=reason)


# Meta Events
class MetaEvent(Event):
    """元事件"""
    __event__ = "meta_event"
    post_type: Literal["meta_event"]
    meta_event_type: str

    @overrides(Event)
    def get_event_name(self) -> str:
        sub_type = getattr(self, "sub_type", None)
        return f"{self.post_type}.{self.meta_event_type}" + (f".{sub_type}" if
                                                             sub_type else "")

    @overrides(Event)
    def get_log_string(self) -> str:
        raise NoLogException


class LifecycleMetaEvent(MetaEvent):
    """生命周期元事件"""
    __event__ = "meta_event.lifecycle"
    meta_event_type: Literal["lifecycle"]
    sub_type: str


class HeartbeatMetaEvent(MetaEvent):
    """心跳元事件"""
    __event__ = "meta_event.heartbeat"
    meta_event_type: Literal["heartbeat"]
    status: Status
    interval: int


_t = StringTrie(separator=".")

# define `model` first to avoid globals changing while `for`
model = None
for model in globals().values():
    if not inspect.isclass(model) or not issubclass(model, Event):
        continue
    _t["." + model.__event__] = model


def get_event_model(event_name) -> List[Type[Event]]:
    """
    :说明:

      根据事件名获取对应 ``Event Model`` 及 ``FallBack Event Model`` 列表

    :返回:

      - ``List[Type[Event]]``
    """
    return [model.value for model in _t.prefixes("." + event_name)][::-1]


__all__ = [
    "Event", "MessageEvent", "PrivateMessageEvent", "GroupMessageEvent",
    "MessageSentEvent", "PrivateMessageSentEvent", "GroupMessageSentEvent",
    "NoticeEvent", "GroupUploadNoticeEvent", "GroupAdminNoticeEvent",
    "GroupDecreaseNoticeEvent", "GroupIncreaseNoticeEvent",
    "GroupBanNoticeEvent", "FriendAddNoticeEvent", "GroupRecallNoticeEvent",
    "FriendRecallNoticeEvent", "NotifyEvent", "FriendPokeNotifyEvent",
    "GroupPokeNotifyEvent", "LuckyKingNotifyEvent", "HonorNotifyEvent",
    "GroupCardNoticeEvent", "OfflineFileNoticeEvent",
    "ClientStatusNoticeEvent", "EssenceMessageNoticeEvent", "RequestEvent",
    "FriendRequestEvent", "GroupRequestEvent", "MetaEvent",
    "LifecycleMetaEvent", "HeartbeatMetaEvent", "get_event_model"
]
