# Flutter Server

使用Python写的Flutter Server端

通过接受Flutter Client发送过来的JSON数据进行解析操作

## 环境要求

- Python3.10及以上版本

## 使用说明
安装项目依赖包
```bash
pip310 install -r requirements.txt
```
运行
```bash
python310 flutter.py
```
测试
```bash
# 在/tmp/create_and_delete/目录下新建文件
nc 127.0.0.1 8080 <<< '{"operation":"create","directory":"/tmp/create_and_delete/"}'

# 在/tmp/create_and_delete/目录下随机删除文件
nc 127.0.0.1 8080 <<< '{"operation":"delete","directory":"/tmp/create_and_delete/"}'

# 在/tmp/create_and_modify/目录下新建文件
nc 127.0.0.1 8080 <<< '{"operation":"create","directory":"/tmp/create_and_modify/"}'

# 在/tmp/create_and_modify/目录下随机修改文件
nc 127.0.0.1 8080 <<< '{"operation":"modify","directory":"/tmp/create_and_modify/"}'
```

监控目录文件
```
watch -n 1 ls -l /tmp/create_and_delete/

watch -n 1 ls -l /tmp/create_and_modify/
```
