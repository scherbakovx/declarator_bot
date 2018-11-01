# -*- coding: utf-8 -*-
import json


def validate_request(query):
    """
    Check that request query is ok.
    """
    query_length = len(query.split())
    if query_length <= 3 and query_length >= 1:
        return True
    return False


def parse_search_answer(data):
    """
    Method check returned data from request.
    Return is amount of answers _, result _.
    """
    if isinstance(data, bytes):
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)

    if isinstance(data, list):
        return 0, "Неверный формат запроса."
    elif isinstance(data, dict):
        count = data['count']
        if count == 0:
            return count, "Результатов не найдено."
        elif count == 1:
            result = data['results'][0]['id']
            return count, result
        elif count <= 25:
            result = [{'text': get_office_position(person), 'id': person.get(
                'id')} for person in data['results']]
            return count, result
        else:
            return count, "Очень много."
    else:
        # привет
        return 0, "Что-то странное."


def get_office_position(person):
    information = person.get('sections', [])
    if information:
        last_information = information[0]
        return "%s / %s" % (last_information.get('office'), last_information.get('position'))
    return None


def get_templated_string(field_name, obj, template):
    if field_name == 'Транспортные средства':
        return template % (obj['type']['name'])
    elif field_name == 'Недвижимое имущество':
        return template % (obj['type']['name'], obj['square'], obj.get('own_type', {}).get('name', ''))
    elif field_name == 'Доход':
        return template % (obj['size'], obj['comment'])
    return


def create_part_of_answer(field_name, data, template):
    result = "\n*%s*\n" % field_name
    for obj in data:
        if obj['relative'] is None:
            result += "%s\n" % get_templated_string(
                field_name, obj, template)
        else:
            result += "%s: %s\n" % (obj['relative']['name'],
                                    get_templated_string(field_name, obj, template))
    return result


def parse_person_answer(data):
    if isinstance(data, bytes):
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)

    all_years = data['results']
    result = ""
    if all_years:
        last_year = all_years[-1]
        result += "%s\n%s\n" % (last_year['main']['office']
                                ['post'], last_year['main']['office']['name'])

        incomes = last_year['incomes']
        if incomes:
            # maybe no comment
            result += create_part_of_answer("Доход", incomes, "%s руб. (%s)")

        real_estates = last_year['real_estates']
        if real_estates:
            result += create_part_of_answer("Недвижимое имущество",
                                            real_estates, "%s, %s кв. м. (%s)")

        vehicles = last_year['vehicles']
        if vehicles:    # need more information
            result += create_part_of_answer(
                "Транспортные средства", vehicles, "%s")

        savings = last_year['savings']
        if savings:
            result += "\n*Счета*\n"
            for saving in savings:
                result += "%s\n" % saving

        # spendings
        # stocks

    # split result
    return result[:1000]


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
