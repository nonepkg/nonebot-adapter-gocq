<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot-Adapter-GOCQ

_✨ go-cqhttp 协议适配 ✨_

在原 CQHTTP Adapter 的基础上进行了修改以便于更好地适配 go-cqhttp

</div>

### 改动

- 兼容 go-cqhttp 与 Onebot 标准不同的 API、Event、CQ 码

- Request 事件的 approve、adject 方法不再需要 bot 参数

- 当用户为群主时，GROUP_ADMIN 也返回 True

### 版本

版本号与 nonebot-adapter-cqhttp 保持一致，也就是说也会有 .post1 这种东西

如果 go-cqhttp 更新了新的 API/Event/CQ 码，也只能在下个版本跟着一起更新了
