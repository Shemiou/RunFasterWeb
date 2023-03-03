0| 工作路径
```shell
cd RunFaster/running
```

1| 安装依赖
```shell
pip3 install -r requirements.txt
playwright install
```

2| 启动Django
```shell
cd RunFaster

python manage.py runserver 127.0.0.1:9007
```

3| 进入后台
```浏览器访问
http://127.0.0.1:9007/index
```
[后台地址]()

4| 执行操作
>  运行全用例 、 运行单条用例、 查看报告
[测试报告]()