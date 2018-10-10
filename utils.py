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
    if isinstance(data, list):
        return 0, "Неверный формат запроса."
    elif isinstance(data, dict):
        count = data['count']
        if count == 0:
            return count, "Результатов не найдено."
        elif count == 1:
            result = data['results']['id']
            return count, result
        elif count <= 25:
            result = [get_office_position(person) for person in data['results']]
            return count, result
        else:
            return count, "Очень много."
    else:
        return 0, "Что-то странное."

def get_office_position(person):
    information = person.get('sections', [])
    if information:
        last_information = information[0]
        return "%s / %s" % (last_information.get('office'), last_information.get('position'))
    return None
    
def parse_person_answer(data):
    return data['count']