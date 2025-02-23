#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: session.py
@date: 2024 2024/9/12 21:56
@desc: 
"""
from urllib.parse import urljoin
import logging
import requests
import allure
from requests import Response, PreparedRequest


logger = logging.getLogger("requests.session")
logging.basicConfig(level=logging.INFO)


class Session(requests.Session):
    def __init__(self, base_url=None):
        super().__init__()  # 先执行父类的初始化
        self.base_url = base_url  # 在执行子类的初始化操作

    @allure.step("发送请求")
    def request(self, method, url: str, *args, **kwargs) -> Response:
        if not url.startswith("http"):
            # 自动添加baseurl
            url = urljoin(self.base_url, url)
        return super().request(method, url, *args, **kwargs)  # 按照原有方式执行

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        logger.info(f"发送请求>>>>>> 接口地址 = {request.method} {request.url}")
        logger.info(f"发送请求>>>>>> 请求头 = {request.headers}")
        logger.info(f"发送请求>>>>>> 请求正文 = {request.body} ")

        resp = super().send(request, **kwargs)  # 按照原有方式发送请求

        logger.info(f"接收响应      <<<<<< 状态码 = {resp.status_code}")
        logger.info(f"接收响应      <<<<<< 响应头 = {resp.headers}")
        logger.info(f"接收响应      <<<<<< 响应正文 = {resp.json()}")

        return resp


if __name__ == '__main__':
    ...
