# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   加载config.ini配置你信息

import configparser
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def get_node_info(sec_name):
    """
    加载节点配置信息
    :param sec_name: 节点名称
    :return: 节点所有属性信息 ConfigHandler
    """
    return ConfigHandler(sec_name)


class ConfigHandler:
    """loading config.ini info
    Attributes :
        dst_path : 资源目标路径
        mvn_path : mvn soft path
    """

    __default_options = {"branch_name": "master",
                         "producer_protocol_port_start": 6000,
                         "producer_debug_port_start": 5000,
                         "customer_port_start": 8000,
                         "customer_debug_port_start": 7000,
                         "producer_prefix": "finance-",
                         "producer_suffix": "-service",
                         "customer_prefix": "hk-",
                         "customer_suffix": "-services",
                         "version": "-1.0-SNAPSHOT",
                         "proxy_ssh_port": "22",
                         "debug": 1,
                         "agent": 0,
                         "agent_ip": "192.168.1.249:11800",
                         "backup_suffix": "_backup"}

    def __init__(self, sec_name):
        config_ini_path = os.path.abspath("./config/config.ini")
        self.__config = configparser.ConfigParser()
        self.__config.read(config_ini_path)
        # 节点不在直接抛出异常
        if sec_name not in self.__config.sections():
            raise Exception("node %s no exit" % sec_name)
        # 加载全局配置
        self.dst_path = os.path.abspath(self.__config.get("global", "dst_path"))
        self.mvn_path = self.__config.get("global", "mvn_path")
        self.ln_log_dst_path = self.__config.get("global", "ln_log_dst_path")
        logging.debug("*****global config info*************************")
        logging.debug("*dst_path=%s, mvn_path=%s, ln_log_dst_path=%s" % (self.dst_path, self.mvn_path, self.ln_log_dst_path))
        logging.debug("*****global config info*************************")
        # 加载jenkins配置
        self.config_xml_path = os.path.abspath(self.__config.get("jenkins", "config_xml_path"))
        self.job_dst_path = os.path.abspath(self.__config.get("jenkins", "job_dst_path"))
        logging.debug("*****jenkins config info************************")
        logging.debug("*config_xml_path=%s, job_path=%s" % (self.config_xml_path, self.job_dst_path))
        logging.debug("*****jenkins config info************************")
        self.__get_config(sec_name)

    def __get_config(self, sec_name):
        """
        加载指定sec_name节点信息
        :param sec_name: 节点名称
        """
        self.sec_name = sec_name
        self.src_path = os.path.abspath(self.__get_value("src_path"))
        self.env_path = os.path.abspath(self.__get_value("env_path"))
        self.producer_list = self.__get_value("producer_list").split(",")
        self.producer_protocol_port_start = int(self.__get_value("producer_protocol_port_start"))
        self.producer_debug_port_start = int(self.__get_value("producer_debug_port_start"))
        self.customer_list = self.__get_value("customer_list").split(",")
        self.customer_port_start = int(self.__get_value("customer_port_start"))
        self.customer_debug_port_start = int(self.__get_value("customer_debug_port_start"))
        self.proxy_tomcat_port = self.__get_value("proxy_tomcat_port")
        self.proxy_zk_port = self.__get_value("proxy_zk_port")
        self.proxy_ssh_port = self.__get_value("proxy_ssh_port")
        self.debug = self.__get_value("debug")
        self.agent = self.__get_value("agent")
        self.agent_ip = self.__get_value("agent_ip")
        self.branch_name = self.__get_value("branch_name")
        self.backup_suffix = self.__get_value("backup_suffix")
        self.producer_prefix = self.__get_value("producer_prefix")
        self.producer_suffix = self.__get_value("producer_suffix")
        self.customer_prefix = self.__get_value("customer_prefix")
        self.customer_suffix = self.__get_value("customer_suffix")
        self.version = self.__get_value("version")
        logging.debug("*****node config info***************************")
        logging.debug("agent=%s" % self.agent)
        logging.debug("*src_path=%s, env_path=%s, producer_list=%s, customer_list=%s, branch_name=%s, proxy_tomcat_port=%s, backup_suffix=%s" % (self.src_path, self.env_path, self.producer_list, self.customer_list, self.branch_name, self.proxy_tomcat_port, self.backup_suffix))
        logging.debug("*****node config info***************************")

    def __get_value(self, option):
        if self.__config.has_option(self.sec_name, option) and self.__config.get(self.sec_name, option) != "":
            return self.__config.get(self.sec_name, option)
        else:
            return self.__default_options[option]

    def get_module_name(self, service_name):
        """
        获取服务模块名称
        :param service_name: 服务简称
        :return: 服务名称
        """
        if self.producer_list.count(service_name):
            return "finance-" + service_name
        return "hk-" + service_name + "-services"

    def get_pom_path(self, service_name):
        """
        获取服务对应的pom文件
        :param service_name: 服务简称
        :return: pom.xml绝对路径
        """
        if not service_name:
            return self.src_path + "/pom.xml"
        if self.producer_list.count(service_name):
            return self.src_path + "/finance-" + service_name + "/pom.xml"
        return self.src_path + "/hk-" + service_name + "-services/pom.xml"

    def get_copy_src_path(self, service_name):
        """
        获取指定服务jar、war绝对路径
        :param service_name: 服务简称
        :return: jar、war路径
        """
        if self.producer_list.count(service_name):
            return self.src_path + "/finance-" + service_name + "/finance-" + service_name + "-service/target/" + service_name + "-1.0-SNAPSHOT.jar"
        return self.src_path + "/hk-" + service_name + "-services/target/hk-" + service_name + "-services.war"

    def get_copy_dst_path(self, service_name):
        """
        获取指定服务目标路径
        :param service_name: 服务简称 
        :return: 路径
        """
        if self.producer_list.count(service_name):
            return self.dst_path + "/finance-" + service_name + "-service/" + service_name + ".jar"
        return self.src_path + "/hk-" + service_name + "-services/webapps/" + service_name + ".war"

    def get_common_resources_path(self):
        """
        获取源码项目公共资源路径
        :return: 资源绝对路径
        """
        return self.src_path + os.path.sep + "env"

    def get_service_resources_path(self, service_name):
        """
        获取指定服务源码项目的资源路径
        :param service_name: 服务名称
        :return: 资源绝对路径
        """
        return str(self.src_path + "/fiance-#/finance-#-services/src/main/resources/env").replace("#", service_name)

    def get_web_resources_path(self, service_name):
        """
        获取指定web服务源码项目的资源路径
        :param service_name: 服务名称
        :return: 资源绝对路径
        """
        return str(self.src_path + "/hk-#-services/src/main/resources/env").replace("#", service_name)
