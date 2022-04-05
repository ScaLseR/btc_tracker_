import json
import requests


class BtcApi:
    """класс для работы с внешним Api https://old.coindesk.com/coindesk-api"""
    def __init__(self, n_interval):
        self._url = 'https://old.coindesk.com/coindesk-api'
        self._n_interval = n_interval

    def _request(self, start, end) -> dict:
        """get запрос к API"""
        response = requests.get(self._url, params={'start': start, 'end': end})
        resp = json.loads(response.content)
        dict_resp = {}
        for key, value in resp['bpi'].items():
            dict_resp[key] = value
        return dict_resp

    def _gap_cutting(self, start, end):
        """"""
        pass

    def load_start_end(self, start, end):
        """получение данных от API в промежутке start -> end"""
        pass

    def load_start_n_days(self, start, n_days: int):
        """получение данных от API от начала start и на N дней"""
        pass
