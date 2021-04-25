import os
import time
from datetime import datetime

from backends.settings import LOG_PATH, UN_LOG_PATH
from utils.utils import create_folder


def handle_request(request):
    try:
        request_user = request.user.name
        request_path = request.get_full_path()
        request_datetime = datetime.now()
        request_method = request.method
        request_data = request.body
        log_info = f"{request_datetime}\t{'Request'}\t{request_user}\t{request_method}\t{request_path}\t{request_data}"
    except Exception as ex:
        log_info = f"{str(ex)}"
    write_log(log_info)


def handle_response(response):
    # 获取响应中的request信息
    try:
        response_request = response.renderer_context['request']
        response_user = response_request.user.name
        response_full_path = response_request.get_full_path()
        response_path = response_request.path
        response_datetime = datetime.now()
        response_method = response_request.method
        if response_path in UN_LOG_PATH:
            response_data = {'该接口响应数据不显示，详情参考settings.py中UN_LOG_PATH'}
        else:
            response_data = response.data
        log_info = f"{response_datetime}\t{'Response'}\t{response_user}\t{response_method}\t{response_full_path}" \
                   f"\t{response_data}"
    except Exception as ex:
        log_info = f"{str(ex)}"
    write_log(log_info)


def write_log(log_info):
    timestamp = time.localtime(time.time())
    log_path = os.path.join(LOG_PATH, time.strftime('%Y', timestamp))
    create_folder(log_path)
    log_name = time.strftime('%Y-%m-%d', timestamp) + '.log'

    full_log_path = os.path.join(log_path, log_name)

    with open(full_log_path, 'a', encoding='utf-8') as f:
        f.write(log_info + '\n')
