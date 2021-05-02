import re
from functools import reduce
from typing import Any, Dict, Literal, Union, Tuple, Mapping, Iterable, Optional

from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment

from .utils import log, escape, unescape, _b2s


class MessageSegment(BaseMessageSegment):
    """
    go-cqhttp 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @overrides(BaseMessageSegment)
    def __init__(self, type: str, data: Dict[str, Any]) -> None:
        super().__init__(type=type, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        type_ = self.type
        data = self.data.copy()

        # process special types
        if type_ == "text":
            return escape(
                data.get("text", ""),  # type: ignore
                escape_comma=False)

        params = ",".join(
            [f"{k}={escape(str(v))}" for k, v in data.items() if v is not None])
        return f"[CQ:{type_}{',' if params else ''}{params}]"

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return (MessageSegment.text(other)
                if isinstance(other, str) else Message(other)) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def face(id_: int) -> "MessageSegment":
        return MessageSegment("face", {"id": str(id_)})

    @staticmethod
    def record(file: str,
               magic: Optional[bool] = None,
               cache: Optional[bool] = None,
               proxy: Optional[bool] = None,
               timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            "record", {
                "file": file,
                "magic": _b2s(magic),
                "cache": _b2s(cache),
                "proxy": _b2s(proxy),
                "timeout": timeout
            })

    @staticmethod
    def video(file: str,
              cover: Optional[str] = None,
              c_: int = 1) -> "MessageSegment":
        return MessageSegment("video", {
            "file": file,
            "cover": cover,
            "c_": c_
        })

    @staticmethod
    def at(qq: Union[int, str], name: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("at", {"qq": str(qq), "name": name})

    @staticmethod
    def rps() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("rps", {})

    @staticmethod
    def dice() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("dice", {})

    @staticmethod
    def shake() -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("shake", {})

    @staticmethod
    def anonymous(ignore_failure: Optional[bool] = None) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("anonymous", {"ignore": _b2s(ignore_failure)})

    @staticmethod
    def share(url: str = "",
              title: str = "",
              content: Optional[str] = None,
              image: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("share", {
            "url": url,
            "title": title,
            "content": content,
            "image": image
        })

    @staticmethod
    def contact(type_: str, id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("contact", {"type": type_, "id": str(id)})

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("contact", {"type": "group", "id": str(group_id)})

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment("contact", {"type": "qq", "id": str(user_id)})

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: Optional[str] = None,
                 content: Optional[str] = None) -> "MessageSegment":
        """
        该 CQcode 暂未被 go-cqhttp 支持。
        """
        return MessageSegment(
            "location", {
                "lat": str(latitude),
                "lon": str(longitude),
                "title": title,
                "content": content
            })

    @staticmethod
    def music(type_: str, id_: int) -> "MessageSegment":
        return MessageSegment("music", {"type": type_, "id": id_})

    @staticmethod
    def music_custom(url: str,
                     audio: str,
                     title: str,
                     content: Optional[str] = None,
                     image: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "music", {
                "type": "custom",
                "url": url,
                "audio": audio,
                "title": title,
                "content": content,
                "image": image
            })

    @staticmethod
    def image(file: str,
              type_: Optional[Literal["flash", "show"]] = None,
              cache: bool = True,
              id_: int = 40000,
              c_: int = 1) -> "MessageSegment":
        return MessageSegment(
            "image", {
                "file": file,
                "type": type_,
                "cache": cache,
                "id_": id_,
                "c_": c_
            })

    @staticmethod
    def reply(id_: int,
              text: Optional[str] = None,
              qq: Optional[int] = None,
              time: Optional[int] = None,
              seq: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            "reply", {
                "id": str(id_),
                "text": text,
                "qq": str(qq),
                "time": str(time),
                "seq": str(seq)
            })

    @staticmethod
    def poke(qq: Union[int, str]) -> "MessageSegment":
        return MessageSegment("poke", {"qq": str(qq)})

    @staticmethod
    def gift(qq: Union[int, str], id_: Union[int, str]) -> "MessageSegment":
        return MessageSegment("poke", {"qq": str(qq), "id": str(id_)})

    @staticmethod
    def forward(id_: str) -> "MessageSegment":
        log("WARNING", "Forward Message only can be received!")
        return MessageSegment("forward", {"id": id_})

    @staticmethod
    def node(id_: int,
             name: Optional[str] = None,
             uin: Optional[int] = None,
             content: Optional["MessageSegment"] = None,
             seq: Optional["MessageSegment"] = None) -> "MessageSegment":
        return MessageSegment(
            "node",{
                "id": str(id_),
                "name": name,
                "uin": str(uin),
                "content": content,
                "seq": seq
            })

    @staticmethod
    def xml(data: str, resid: Optional[int] = None) -> "MessageSegment":
        return MessageSegment("xml", {"data": data, "resid": resid})

    @staticmethod
    def json(data: str, resid: Optional[int] = None) -> "MessageSegment":
        return MessageSegment("json", {"data": data, "resid": resid})

    @staticmethod
    def cardimage(file: str, 
                  minwidth: int = 400, 
                  minheight: int = 400,
                  maxwidth: int = 500,
                  maxheight: int = 1000,
                  source: Optional[str] = None,
                  icon: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "cardimage", {
                "file": file,
                "minwidth": str(minwidth),
                "minheight": str(minheight),
                "maxwidth": str(maxwidth),
                "maxheight": str(maxheight),
                "source": source,
                "icon": icon
            }) 

    @staticmethod
    def tts(text: str) -> "MessageSegment":
        return MessageSegment("tts", {"text": text})

class Message(BaseMessage):
    """
    go-cqhttp 协议 Message 适配。
    """

    def __radd__(self, other: Union[str, MessageSegment,
                                    "Message"]) -> "Message":
        result = MessageSegment.text(other) if isinstance(other, str) else other
        return super(Message, self).__radd__(result)

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping,
                   Iterable[Mapping]]) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, Iterable) and not isinstance(msg, str):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return
        elif isinstance(msg, str):

            def _iter_message(msg: str) -> Iterable[Tuple[str, str]]:
                text_begin = 0
                for cqcode in re.finditer(
                        r"\[CQ:(?P<type>[a-zA-Z0-9-_.]+)"
                        r"(?P<params>"
                        r"(?:,[a-zA-Z0-9-_.]+=[^,\]]+)*"
                        r"),?\]", msg):
                    yield "text", msg[text_begin:cqcode.pos + cqcode.start()]
                    text_begin = cqcode.pos + cqcode.end()
                    yield cqcode.group("type"), cqcode.group("params").lstrip(
                        ",")
                yield "text", msg[text_begin:]

            for type_, data in _iter_message(msg):
                if type_ == "text":
                    if data:
                        # only yield non-empty text segment
                        yield MessageSegment(type_, {"text": unescape(data)})
                else:
                    data = {
                        k: unescape(v) for k, v in map(
                            lambda x: x.split("=", maxsplit=1),
                            filter(lambda x: x, (
                                x.lstrip() for x in data.split(","))))
                    }
                    yield MessageSegment(type_, data)

    def extract_plain_text(self) -> str:

        def _concat(x: str, y: MessageSegment) -> str:
            return f"{x} {y.data['text']}" if y.is_text() else x

        plain_text = reduce(_concat, self, "")
        return plain_text[1:] if plain_text else plain_text
