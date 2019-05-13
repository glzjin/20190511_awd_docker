# 20190511_awd_docker

## 说明

2019 年 5 月 11 日去防灾科技学院打 “应急挑战杯” 大学生网络安全邀请赛的 AWD 靶机题目。

- 1号靶机为 PWN。
- 2号靶机为 Nginx + Python（Flask）题。
- 3号靶机为 Apache + PHP(ThinkPHP5) 题。
- 4号靶机为 Nginx + PHP 题。

## 使用方法

```
docker-compose up -d --build
```

即可创建四个容器，默认对外暴露服务端口和 SSH 端口。

SSH 默认用户名：glzjin 密码：123456
