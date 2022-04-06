import json
import requests
from datetime import datetime, timedelta


class BtcApi:
    """класс для работы с Api https://old.coindesk.com/coindesk-api"""
    def __init__(self, n_interval):
        self._url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
        self._n_interval = n_interval

    def _request(self, start: datetime, end: datetime) -> dict:
        """get запрос к API"""
        print('Выполняем запрос к API с ' + str(start) + ' по ' + str(end))
        response = requests.get(self._url, params={'start': str(start), 'end': str(end)})
        dict_resp = {}
        if not response:
            return dict_resp
        resp = json.loads(response.content)
        for key, value in resp['bpi'].items():
            dict_resp[key] = value
        return dict_resp

    def _gap_cutting(self, start: datetime, end: datetime) -> dict:
        """создаем цепочки дат начало и конец = начало + n"""
        final_dict = {}
        while start + timedelta(days=self._n_interval) < end:
            rez = self._request(start, start + timedelta(days=self._n_interval))
            final_dict.update(rez)
            start += timedelta(days=self._n_interval)
            if start > end:
                start -= timedelta(days=self._n_interval)
                break
        rez = self._request(start, end)
        final_dict.update(rez)
        return final_dict

    def load_start_end(self, start: datetime, end: datetime) -> dict:
        """получение данных от API в промежутке start -> end"""
        if (end - start).days < self._n_interval:
            rez = self._request(start, end)
        else:
            rez = self._gap_cutting(start, end)
        return rez
