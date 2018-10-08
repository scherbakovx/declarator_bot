# -*- coding: utf-8 -*-
import requests
import json


BASE_URL = 'https://declarator.org/api/v1/search/'


def make_request_for_search(query='Иванов'):
    method_url = 'person-sections/?name=%s'
    response = requests.get(BASE_URL + method_url % query)
    if response.status_code == 200:
        data = response.content
        return data
    else:
        # TODO: add error handling
        return


def make_request_for_person(person_id=100):
    method_url = 'sections/?person=%d'
    response = requests.get(BASE_URL + method_url % person_id)
    if response.status_code == 200:
        data = response.content
        return data
    else:
        # TODO: add error handling
        return
