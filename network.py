# -*- coding: utf-8 -*-
import requests
import json


from utils import parse_search_answer

BASE_URL = 'https://declarator.org/api/v1/search/'


def make_request_for_search(query=):
    method_url = 'person-sections/?name=%s'
    response = requests.get(BASE_URL + method_url % query)
    if response.status_code == 200:
        data = response.content
        amount, result = parse_search_answer(data)
        if amount == 1:
            make_request_for_person(result)
        else:
            return amount, result
    else:
        # TODO: add error handling
        return


def make_request_for_person(person_id):
    method_url = 'sections/?person=%d'
    response = requests.get(BASE_URL + method_url % person_id)
    if response.status_code == 200:
        data = response.content
        result = parse_person_answer(data)
        return 1, result
    else:
        # TODO: add error handling
        return
