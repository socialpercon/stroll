#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   文件操作工具类

import re
import os
import logging
import shutil

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def replace(file_path, old_params, new_params):
    """
    替换文件中的关键字
    :param file_path: 文件路径
    :param old_params: 需要替换的旧的关键字
    :param new_params: 新的值
    :return: void
    """
    logging.debug("file file_path: " + file_path + "; old_params: " + ", ".join(old_params) + "; new_params: " + ", ".join(new_params))
    if len(old_params) <= 0 or len(new_params) <= 0:
        print("can't find replace params.")
        return
    read_file = open(file_path, 'r',  encoding="UTF-8")
    content = ""
    for line in read_file:
        for param in old_params:
            if re.search(param, line):
                line = re.sub(param, new_params[old_params.index(param)], line)
        content += line
    read_file.close()
    write_file = open(file_path, 'w',  encoding="UTF-8")
    write_file.write(content)
    write_file.close()


def list_files(file_path, root_name="", child=True):
    """
    查询路径下文件列表
    :param file_path: 根路径
    :param root_name: 子路径名称
    :param child: 是否包括子文件
    :return: 文件列表绝对路径的集合
    """
    file_lists = []
    result = []
    prefix_list = []
    # 加载所有文件
    for root, dirs, files in os.walk(file_path):
        if len(root_name) > 0 and os.path.basename(root) == root_name:
            prefix_list.append(root)
        for f in files:
            file_lists.append(root + os.path.sep + f)

    # 过滤掉不是root_name下的文件
    if len(prefix_list) > 0:
        for p in prefix_list:
            for f in file_lists:
                # if not child and f.replace(p, "").count(os.path.sep) <= 0:
                if f.startswith(p):
                    result.append(f)
        file_lists = result
        result = []

    # 过滤掉child文件
    if not child:
        tmp = file_path
        if len(prefix_list) > 0:
            tmp = prefix_list.pop()
        for f in file_lists:
            if f.replace(tmp, "").count(os.path.sep) <= 1:
                result.append(f)
        file_lists = result
    logging.debug(file_lists)
    return file_lists


def get_parent_path(path):
    """
    获取path的父路径
    :param path: 路径
    :return: 路径
    """
    return os.path.abspath(os.path.join(os.path.abspath(path), os.path.pardir))


def make_dirs(file_path):
    """
    创建路径
    :param file_path: 路径
    :return: None
    """
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        os.makedirs(file_path)


def copy_file(src_file_path, dst_path, only_parent=False):
    """
    拷贝文件，如果dst_path不存在，就创建路径
    :param src_file_path: 源文件路径
    :param dst_path: 目标地址
    :param only_parent: 只创建到dst_path路径
    :return: None
    """
    if only_parent:
        make_dirs(get_parent_path(dst_path))
    else:
        make_dirs(dst_path)
    shutil.copy(src_file_path, dst_path)


def copy_path(src_path, dst_path, remove=False):
    if remove and os.path.exists(dst_path) and os.path.isdir(dst_path):
        shutil.rmtree(dst_path)
    shutil.copytree(src_path, dst_path)


def del_path(path, *file_name):
    """
    删除文件夹或是文件中指定文件
    :param path: 路径
    :param file_name: 具体文件名称 
    :return: None
    """
    logging.debug("del path: " + path + ", special file list is: ")
    logging.debug(file_name)
    path = os.path.abspath(path)
    if os.path.exists(path) and os.path.isdir(path):
        if len(file_name) > 0:
            for root, dirs, files in os.walk(path):
                for a in files:
                    for b in file_name:
                        if a == b:
                            os.remove(os.path.abspath(os.path.join(root, a)))
        else:
            shutil.rmtree(path)


if __name__ == "__main__":
    # replace(os.path.abspath("../output/dst/jobs/hk_master-hk-bi-services/config.xml"), ["stroll_node", "stroll_service"], ["hello", "world"])
    # del_path(os.path.abspath("../output/projects/hk-api-services/src/main/resources/env"))
    # copy_path(os.path.abspath("../output/dst/jobs"), os.path.abspath("../output/projects/jobs"), remove=True)
    # copy_file(os.path.abspath("../output/env/env_hk/env_bi.properties"), os.path.abspath("../output/dst/env_bi.properties"))
    tmp = ""
    if not tmp:
        print("ok")
