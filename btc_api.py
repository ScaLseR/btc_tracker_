import json
import requests
from datetime import datetime


class BtcApi:
    """класс для работы с внешним Api https://old.coindesk.com/coindesk-api"""
    def __init__(self, n_interval):
        self._url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
        self._n_interval = n_interval

    def _request(self, start: datetime, end: datetime) -> dict:
        """get запрос к API"""
        response = requests.get(self._url, params={'start': str(start), 'end': str(end)})
        resp = json.loads(response.content)
        dict_resp = {}
        for key, value in resp['bpi'].items():
            dict_resp[key] = value
        return dict_resp


    def _gap_cutting(self, start, end):
        """"""
        pass

    def load_start_end(self, start: datetime, end: datetime):
        """получение данных от API в промежутке start -> end"""
        if (end - start).days < self._n_interval:
            print('Выполняем запрос к API с ' + str(start) + ' по ' + str(end))
            rez = self._request(start, end)
            return rez

    def load_start_n_days(self, start, n_days: int):
        """получение данных от API от начала start и на N дней"""
        pass
