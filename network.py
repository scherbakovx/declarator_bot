# -*- coding: utf-8 -*-
import requests
import json


from utils import parse_search_answer, parse_person_answer

BASE_URL = 'https://declarator.org/api/v1/search/'


def make_request_for_search(query):
    method_url = 'person-sections/?name=%s'
    response = requests.get(BASE_URL + method_url % query)
    if response.status_code == 200:
        data = response.content
        amount, result = parse_search_answer(data, query)
        if amount == 1:
            amount, data, year = make_request_for_person(result)
            return amount, data, year, result
        else:
            return amount, result, None, None
    elif response.status_code == 400:
        return 0, "Неверный формат запроса.", None, None


def make_request_for_person(person_id):
    method_url = 'sections/?person=%d'
    response = requests.get(BASE_URL + method_url % person_id)
    if response.status_code == 200:
        data = response.content
        result, year = parse_person_answer(data)
        return 1, result, year
    elif response.status_code == 400:
        return 0, "Неверный формат запроса.", None
