import os
import syslog

class SystemD():
    def __init__(self, name='cups'):
        self.name = name

    def isActive(self):
        cmd = f'systemctl is-active --quiet {self.name}.service'
        if os.system(cmd) == 0:
            syslog.syslog(syslog.LOG_INFO, 'Проверка состояние сервиса; Сервис работает.')
            return True
        else:
            syslog.syslog(syslog.LOG_INFO, 'Проверка состояние сервиса; Сервис выключен.')
            return False

    def command(self, command):
        cmd = f'sudo systemctl {command} cups.service'
        if os.system(cmd) == 0:
            syslog.syslog(syslog.LOG_INFO, f'Успешное выполнение: {cmd}')
            return True
        else:
            syslog.syslog(syslog.LOG_ERR, f'Ошибка: {cmd}')
            return False