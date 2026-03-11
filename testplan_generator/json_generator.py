from filter_tests import TestFilter
import json
import os


def check_update_file(file_path: str, data):
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

# def create_testplan_metadata():
#     result = extract_test('./tests')
#     check_update_file('testplans/metadata.json', result)
#     return result


def find_tests(query: str | dict, tests: list) -> list[dict]:
    """
    deserialize filter query,
    collect all tests with metadata,
    filter collected tests by filter
    """
    try:
        json_format = query
        if isinstance(query, str):
            json_format = json.loads(query)
        
        if isinstance(json_format, list):
            if all(len(el.keys()) == 0 for el in json_format):
                return []
        if isinstance(json_format, dict) and not json_format.keys():
            return []
        filter_engine = TestFilter(tests)
        found = filter_engine.filter(json_format)
        return found
    except Exception as e:
        print(f"ERROR: {e}")
        return []

def generate_testplan(results: list):
    template = {"version": "1.0", "tests": [{"id": el['id']} for el in results if el['id']]}
    check_update_file('testplans/testplan.json', template)

# create_testplan_metadata()

# generate_testplan(find_tests(query='{"markers": {"in": ["smoke"]}}'))