import logging
import time
import os
import common.common_util as common_util


class LoggerUtil(object):

    def create_log(self, logger_name=None):
        # 创建一个logger对象
        self.logger = logging.getLogger(logger_name)
        # 设置全局的日志级别
        self.logger.setLevel(logging.DEBUG)
        # 判断日志器中是否存在控制器
        if not self.logger.handlers:
            # 设置file日志文件的路径
            self.log_file_path = common_util.get_path() + "logs/" + common_util.read_config_yaml('log', 'log_name') + \
                                 f'{time.strftime("%Y.%m.%d",time.localtime())}' + '.log'
            # 创建file日志的控制器
            self.file_handler = logging.FileHandler(self.log_file_path, encoding='utf8')
            # 单独的设置文件日志的级别
            file_log_level = common_util.read_config_yaml('log', 'log_level')
            if file_log_level == 'debug':
                self.file_handler.setLevel(logging.DEBUG)
            elif file_log_level == 'info':
                self.file_handler.setLevel(logging.INFO)
            elif file_log_level == 'warning':
                self.file_handler.setLevel(logging.WARNING)
            elif file_log_level == 'error':
                self.file_handler.setLevel(logging.ERROR)
            elif file_log_level == 'critical':
                self.file_handler.setLevel(logging.CRITICAL)
            else:
                pass
            # 设置file日志的格式
            self.file_handler.setFormatter(logging.Formatter(fmt=common_util.read_config_yaml('log', 'log_format')))
            # 将file日志的控制器加入日志对象
            self.logger.addHandler(self.file_handler)
            # print("--------------控制台日志----------------")
            # 创建console日志的控制器
            self.console_handler = logging.StreamHandler()
            # 单独的设置console日志的级别
            console_log_level = common_util.read_config_yaml('log', 'log_level')
            if console_log_level == 'debug':
                self.console_handler.setLevel(logging.DEBUG)
            elif console_log_level == 'info':
                self.console_handler.setLevel(logging.INFO)
            elif console_log_level == 'warning':
                self.console_handler.setLevel(logging.WARNING)
            elif console_log_level == 'error':
                self.console_handler.setLevel(logging.ERROR)
            elif console_log_level == 'critical':
                self.console_handler.setLevel(logging.CRITICAL)
            else:
                pass
            # 设置console日志的格式
            self.console_handler.setFormatter(logging.Formatter(common_util.read_config_yaml('log', 'log_format')))
            # 将console日志的控制器加入日志对象
            self.logger.addHandler(self.console_handler)
        return self.logger

    def remove_logger(self):
        self.logger.removeFilter(self.file_handler)
        self.logger.removeFilter(self.console_handler)


#写入正常日志
def write_log(log_message):
    LoggerUtil().create_log('logger').info(log_message)

#写入异常日志
def write_error_log(log_message):
    LoggerUtil().create_log('logger').info(log_message)
    raise Exception(log_message)


if __name__ == "__main__":
    pass