# 判断IP是否有效

## 依赖

- requests=2.22.0

- proxy.txt：从网上获得的可用IP


## 运行

首先需要在`proxy_judge.py`的`judge_ip(ip)`函数(line:12)第一行修改`http_url`为需要测试的网址。

```shell
$ python3 proxy_judge.py
```

## 结果

- valid.txt：对指定网址可用的IP。

