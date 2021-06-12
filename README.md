<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Adapter GOCQ

_✨ go-cqhttp 协议适配 ✨_

在原 CQHTTP Adapter 的基础上进行了修改以便于更好地适配 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

</div>

## Guide

[使用指南](./docs/manual.md)

## Feature

- [x] 兼容 go-cqhttp 与 Onebot 标准不同的 API、Event、CQCode
- [x] Request 事件的 approve、adject 方法不再需要 bot 参数

## Bug

- [x] 由于 at 的 CQ 码增加了 name 字段导致群里被 at 的 bot 上报的 to_me 字段恒为 false
- [x] 私聊消息遇到错误，没有字段 temp_source
