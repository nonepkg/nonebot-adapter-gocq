import asyncio
from typing import Any, Dict, List, Union, Optional

from nonebot.config import Config
from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Driver, WebSocket

from .event import Event
from .message import Message, MessageSegment


def get_auth_bearer(access_token: Optional[str] = ...) -> Optional[str]:
    ...


async def _check_reply(bot: "Bot", event: Event):
    ...


def _check_at_me(bot: "Bot", event: Event):
    ...


def _check_nickname(bot: "Bot", event: Event):
    ...


def _handle_api_result(result: Optional[Dict[str, Any]]) -> Any:
    ...


class ResultStore:
    _seq: int = ...
    _futures: Dict[int, asyncio.Future] = ...

    @classmethod
    def get_seq(cls) -> int:
        ...

    @classmethod
    def add_result(cls, result: Dict[str, Any]):
        ...

    @classmethod
    async def fetch(cls, seq: int, timeout: Optional[float]) -> Dict[str, Any]:
        ...


class Bot(BaseBot):

    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: WebSocket = None):
        ...

    def type(self) -> str:
        ...

    @classmethod
    async def check_permission(cls, driver: Driver, connection_type: str,
                               headers: dict, body: Optional[dict]) -> str:
        ...

    async def handle_message(self, message: dict):
        ...

    async def call_api(self, api: str, *, self_id: Optional[str],
                       **data) -> Any:
        ...

    async def send(self, event: Event, message: Union[str, Message,
                                                      MessageSegment],
                   **kwargs) -> Any:
        ...

    async def send_private_msg(self,
                               *,
                               user_id: int,
                               group_id: int,
                               message: Union[str, Message],
                               auto_escape: bool = ...,
                               self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``user_id``: ?????? QQ ???
          * ``group_id``: ??????????????????????????????(?????????????????????????????????/??????)
          * ``message``: ??????????????????
          * ``auto_escape``: ?????????????????????????????????????????????????????? CQ ??????????????? ``message`` ???????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def send_group_msg(self,
                             *,
                             group_id: int,
                             message: Union[str, Message],
                             auto_escape: bool = ...,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????

        :??????:

          * ``group_id``: ??????
          * ``message``: ??????????????????
          * ``auto_escape``: ?????????????????????????????????????????????????????? CQ ??????????????? ``message`` ???????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def send_group_forward_msg(self,
                             *,
                             group_id: int,
                             message: List[Dict[str, Any]],
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``message``: ?????????????????????, ????????? CQcode
        """
        ...

    async def send_msg(self,
                       *,
                       message_type: Optional[str] = ...,
                       user_id: Optional[int] = ...,
                       group_id: Optional[int] = ...,
                       message: Union[str, Message],
                       auto_escape: bool = ...,
                       self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ???????????????

        :??????:

          * ``message_type``: ????????????????????? ``private``???``group``?????????????????????????????????????????????????????????????????????????????? ``*_id`` ????????????
          * ``user_id``: ?????? QQ ????????????????????? ``private`` ????????????
          * ``group_id``: ???????????????????????? ``group`` ????????????
          * ``message``: ??????????????????
          * ``auto_escape``: ?????????????????????????????????????????????????????? CQ ??????????????? ``message`` ???????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def delete_msg(self,
                         *,
                         message_id: int,
                         self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????

        :??????:

          * ``message_id``: ?????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_msg(self,
                      *,
                      message_id: int,
                      self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ???????????????

        :??????:

          * ``message_id``: ?????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_forward_msg(self,
                              *,
                              message_id: int,
                              self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????????????????

        :??????:

          * ``message_id``: ???????????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_image(self,
                        *,
                        file: str,
                        self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``file``: ?????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_kick(self,
                             *,
                             group_id: int,
                             user_id: int,
                             reject_add_request: bool = ...,
                             self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: ????????? QQ ???
          * ``reject_add_request``: ???????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_ban(self,
                            *,
                            group_id: int,
                            user_id: int,
                            duration: int = ...,
                            self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: ???????????? QQ ???
          * ``duration``: ???????????????????????????``0`` ??????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_anonymous_ban(self,
                                      *,
                                      group_id: int,
                                      anonymous: Optional[Dict[str, Any]] = ...,
                                      anonymous_flag: Optional[str] = ...,
                                      duration: int = ...,
                                      self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``anonymous``: ???????????????????????????????????????????????????????????? ``anonymous`` ?????????
          * ``anonymous_flag``: ???????????????????????????????????? flag?????????????????????????????????????????????
          * ``duration``: ?????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_whole_ban(self,
                                  *,
                                  group_id: int,
                                  enable: bool = ...,
                                  self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``group_id``: ??????
          * ``enable``: ????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_admin(self,
                              *,
                              group_id: int,
                              user_id: int,
                              enable: bool = ...,
                              self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: ????????????????????? QQ ???
          * ``enable``: ``True`` ????????????``False`` ?????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_anonymous(self,
                                  *,
                                  group_id: int,
                                  enable: bool = ...,
                                  self_id: Optional[int] = ...) -> None:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ???????????????

        :??????:

          * ``group_id``: ??????
          * ``enable``: ????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_card(self,
                             *,
                             group_id: int,
                             user_id: int,
                             card: str = ...,
                             self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????????????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: ???????????? QQ ???
          * ``card``: ????????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_name(self,
                             *,
                             group_id: int,
                             group_name: str,
                             self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????

        :??????:

          * ``group_id``: ??????
          * ``group_name``: ?????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_leave(self,
                              *,
                              group_id: int,
                              is_dismiss: bool = ...,
                              self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????

        :??????:

          * ``group_id``: ??????
          * ``is_dismiss``: ???????????????????????????????????????????????????????????? True ???????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_special_title(self,
                                      *,
                                      group_id: int,
                                      user_id: int,
                                      special_title: str = ...,
                                      duration: int = ...,
                                      self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ???????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: ???????????? QQ ???
          * ``special_title``: ????????????????????????????????????????????????????????????
          * ``duration``: ????????????????????????????????????-1 ???????????????????????????????????????????????????????????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_friend_add_request(self,
                                     *,
                                     flag: str,
                                     approve: bool = ...,
                                     remark: str = ...,
                                     self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``flag``: ?????????????????? flag????????????????????????????????????
          * ``approve``: ??????????????????
          * ``remark``: ???????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_add_request(self,
                                    *,
                                    flag: str,
                                    sub_type: str,
                                    approve: bool = ...,
                                    reason: str = ...,
                                    self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ??????????????????????????????

        :??????:

          * ``flag``: ??????????????? flag????????????????????????????????????
          * ``sub_type``: ``add`` ??? ``invite``????????????????????????????????????????????? ``sub_type`` ???????????????
          * ``approve``: ???????????????????????????
          * ``reason``: ???????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_login_info(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_stranger_info(self,
                                *,
                                user_id: int,
                                no_cache: bool = ...,
                                self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``user_id``: QQ ???
          * ``no_cache``: ??????????????????????????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_friend_list(self,
                              *,
                              self_id: Optional[int] = ...
                             ) -> List[Dict[str, Any]]:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_info(self,
                             *,
                             group_id: int,
                             no_cache: bool = ...,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????

        :??????:

          * ``group_id``: ??????
          * ``no_cache``: ??????????????????????????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_list(self,
                             *,
                             self_id: Optional[int] = ...
                            ) -> List[Dict[str, Any]]:
        """
        :??????:

          ??????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_member_info(
            self,
            *,
            group_id: int,
            user_id: int,
            no_cache: bool = ...,
            self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``user_id``: QQ ???
          * ``no_cache``: ??????????????????????????????????????????????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_member_list(
            self,
            *,
            group_id: int,
            self_id: Optional[int] = ...) -> List[Dict[str, Any]]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_honor_info(self,
                                   *,
                                   group_id: int,
                                   type: str = ...,
                                   self_id: Optional[int] = ...
                                  ) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``type``: ??????????????????????????????????????? ``talkative`` ``performer`` ``legend`` ``strong_newbie`` ``emotion`` ????????????????????????????????????????????????????????? ``all`` ??????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_cookies(self,
                          *,
                          domain: str = ...,
                          self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ?????? Cookies???

        :??????:

          * ``domain``: ???????????? cookies ?????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_csrf_token(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ?????? CSRF Token???

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_credentials(self,
                              *,
                              domain: str = ...,
                              self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ?????? QQ ?????????????????????

        :??????:

          * ``domain``: ???????????? cookies ?????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_record(self,
                         *,
                         file: str,
                         out_format: str,
                         self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ???????????????

        :??????:

          * ``file``: ???????????????????????????CQ ?????? ``file`` ??????????????? ``0B38145AA44505000B38145AA4450500.silk``
          * ``out_format``: ???????????????????????????????????? ``mp3``???``amr``???``wma``???``m4a``???``spx``???``ogg``???``wav``???``flac``
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def can_send_image(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def can_send_record(self,
                              *,
                              self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_version_info(self,
                               *,
                               self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_restart(self,
                          *,
                          delay: int = ...,
                          self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????? go-cqhttp???

        :??????:

          * ``delay``: ??????????????????????????????????????????????????????????????????????????????????????? 2000 ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def clean_cache(self, *, self_id: Optional[int] = ...) -> None:
        """
        ??? API ????????? go-cqhttp ?????????

        :??????:

          ?????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_group_portrait(self,
                                 *,
                                 group_id: int,
                                 file: str,
                                 cache: int,
                                 self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ??????????????????

        :??????:

          * ``group_id``: ??????
          * ``file``: ???????????????
          * ``cache``: ????????????????????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def ocr_image(self,
                        *,
                        image: str,
                        self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????? OCR???

        :??????:

          * ``image``: ?????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_system_msg(self,
                                   *,
                                   self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def upload_group_file(self,
                                *,
                                group_id: int,
                                file: str,
                                name: str,
                                folder: str,
                                self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ??????????????????

        :??????:
          * ``group_id``: ??????
          * ``file``: ??????????????????
          * ``name``: ????????????
          * ``folder``: ?????????ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_file_system_info(self,
                                         *,
                                         group_id: int,
                                         self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:
          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_root_files(self,
                                   *,
                                   group_id: int,
                                   self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????????????????

        :??????:
          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_files_by_folder(self,
                                        *,
                                        group_id: int,
                                        folder_id: str,
                                        self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ?????????????????????????????????

        :??????:
          * ``group_id``: ??????
          * ``folder_id``: ????????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_file_url(self,
                                 *,
                                 group_id: int,
                                 file_id: str,
                                 busid: int,
                                 self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:
          * ``group_id``: ??????
          * ``folder_id``: ?????? ID
          * ``busid``: ????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_file_url(self,
                                 *,
                                 group_id: int,
                                 file_id: str,
                                 busid: int,
                                 self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:
          * ``group_id``: ??????
          * ``folder_id``: ?????? ID
          * ``busid``: ????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_status(self,
                         *,
                         self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ???????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_at_all_remain(self,
                                      *,
                                      group_id: int,
                                      self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????? @???????????? ???????????????

        :??????:
          
          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def _get_vip_info(self,
                            *,
                            user_id: int,
                            self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????VIP?????????

        :??????:
          
          * ``user_id``: QQ ???
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def _send_group_notice(self,
                                 *,
                                 group_id: int,
                                 content: str,
                                 self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ??????????????????

        :??????:
          
          * ``group_id``: ??????
          * ``content``: ????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def reload_event_filter(self,
                                 *,
                                 self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``self_id``: ????????? QQ ???
        """
        ...

    async def download_file(self,
                            *,
                            url: str,
                            thread_count: int,
                            headers: Union[str, List[str]],
                            self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:

          * ``url``: ????????????
          * ``thread_count``: ???????????????
          * ``headers``: ??????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_online_clients(self,
                                 *,
                                 no_cache: bool,
                                 self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????????????????

        :??????:

          * ``no_cache``: ??????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_group_msg_history(self,
                                    *,
                                    message_seq: int,
                                    group_id: int,
                                    self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ??????????????????????????????

        :??????:

          * ``message_seq``: ??????????????????, ????????? get_msg ??????
          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def set_essence_msg(self,
                              *,
                              message_id: int,
                              self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``message_id``: ?????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def delete_essence_msg(self,
                                 *,
                                 message_id: int,
                                 self_id: Optional[int] = ...) -> None:
        """
        :??????:

          ?????????????????????

        :??????:

          * ``message_id``: ?????? ID
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def get_essence_msg_list(self,
                                   *,
                                   group_id: int,
                                   self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ???????????????????????????

        :??????:

          * ``group_id``: ??????
          * ``self_id``: ????????? QQ ???
        """
        ...

    async def check_url_safely(self,
                               *,
                               url: str,
                               self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :??????:

          ????????????????????????

        :??????:

          * ``url``: ?????????????????????
          * ``self_id``: ????????? QQ ???
        """
        ...
