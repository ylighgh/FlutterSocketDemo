#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import os
import time
import hashlib
import random
from happy_python import *


def gen_range_int_num(form: int, to: int) -> int:
    """
    随机生成指定范围内的整数
    :param form: 起始值
    :param to: 终止值
    :return:
    """
    return int(random.uniform(form, to))


def gen_json_message(status_code: str, message: str) -> None:
    """
    构造JSON格式的消息
    :param status_code: str
    :param message: str
    :return:
    """
    return dict_to_pretty_json({"code": status_code, "message": message}).encode("utf-8")


def create_file(directory: str) -> bool:
    """
    创建新文件
    :param directory: str
    :return:
    """
    flag = True
    has_directory = os.path.exists(directory)
    file_name = gen_md5_32_hexdigest(gen_random_str())
    if has_directory:
        open(directory + file_name, "a").close()
    else:
        os.mkdir(directory)
        open(directory + file_name, "a").close()
    return flag


def delete_file(directory: str) -> int:
    """
    删除文件
    :param directory: str
    :return: flag: int
    1:删除成功
    2:删除失败,文件夹为空
    3:只能对delete文件夹进行删除操作
    """
    flag = 1
    file_list = os.listdir(directory)
    file_list_len = len(file_list)
    if directory != "/tmp/create_and_delete/":
        flag = 3
    else:
        if file_list_len == 0:
            flag = 2
        else:
            file_index = gen_range_int_num(0, file_list_len)
            os.remove(directory + file_list[file_index])
    return flag


def modify_file(directory: str) -> int:
    """
    修改文件内容
    :param directory: str
    :return:
    1:修改成功
    2:修改失败,文件夹为空
    3:只能对modify文件夹进行更改操作
    """
    flag = 1
    file_list = os.listdir(directory)
    file_list_len = len(file_list)
    if directory != "/tmp/create_and_modify/":
        flag = 3
    else:
        if file_list_len == 0:
            flag = 2
        else:
            file_index = gen_range_int_num(0, file_list_len)
            file = directory + file_list[file_index]
            with open(file, mode="a") as f:
                f.write(gen_random_str())
    return flag


def create_server():
    """
    建立连接
    """
    HOST = "0.0.0.0"
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"服务器地址:{HOST}  端口号:{PORT}")
    return s


def connect_client(s):
    """
    传输数据
    """
    while True:
        conn, addr = s.accept()
        recv_data_dic = str_to_dict(conn.recv(4096).decode("utf-8"))

        operation = recv_data_dic["operation"]
        directory = recv_data_dic["directory"]

        if directory != "/tmp/create_and_modify/" and directory != "/tmp/create_and_delete/":
            conn.send(gen_json_message("500", "文件夹错误"))
        else:
            match operation:
                case "create":
                    if create_file(directory):
                        conn.send(gen_json_message("200", "创建文件成功"))
                    else:
                        conn.send(gen_json_message("500", "创建文件失败"))

                case "delete":
                    result = delete_file(directory)
                    if result == 1:
                        conn.send(gen_json_message("200", "删除文件成功"))
                    elif result == 2:
                        conn.send(gen_json_message("500", "删除文件失败,文件夹中没有文件了"))
                    else:
                        conn.send(gen_json_message("500", "仅可以对delete文件夹进行删除操作"))

                case "modify":
                    result = modify_file(directory)
                    if result == 1:
                        conn.send(gen_json_message("200", "修改文件成功"))
                    elif result == 2:
                        conn.send(gen_json_message("500", "修改文件失败,文件夹中没有文件了"))
                    else:
                        conn.send(gen_json_message("500", "仅可以对modify文件夹进行修改操作"))

                case _:
                    conn.send(gen_json_message("500", "操作指令错误"))

        conn.close()


def main():
    s = create_server()
    connect_client(s)
    s.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n收到退出信号,停止运行!")
