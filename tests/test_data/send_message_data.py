import random
from test_data.user_data import valid_names, valid_emails, valid_phones, invalid_emails, invalid_names, invalid_phones

required_inputs = [
    {
        "name": "name",
        "type": "input",
        "find_by": {"id": "name", "name": "name"},
        "props": {"maxlength": 100, "minlength": 2},
    },
    {
        "name": "email",
        "type": "input",
        "find_by": {"id": "email", "name": "email"},
        "props": {"maxlength": 254, "minlength": 5},    # 64 before@
    },
    {
        "name": "telefon",
        "type": "input",
        "find_by": {"id": "telefon", "name": "telefon"},
        "props": {"maxlength": 50, "minlength": 3},
    },
    # {"name": "kezdes", "type": "select", "find_by": {"id": "kezdes", "name": "kezdes"}},
    {"name": "honnan", "type": "select", "find_by": {"id": "honnan", "name": "honnan"}},
    {"name": "captcha", "type": "input", "find_by": {"name": "scode"}, "props": {"maxlength": 2, "minlength": 1}},
]

random_values = [
    {"name": "name", "type": "input", "value": random.choice(valid_names)},
    {"name": "email", "type": "input", "value": random.choice(valid_emails)},
    {"name": "telefon", "type": "input", "value": random.choice(valid_phones)},
    {"name": "honnan", "type": "select", "value": random.randint(1, 4)},
]

random_invalid = [
    {"name": "name", "type": "input", "value": random.choice(invalid_names)},
    {"name": "email", "type": "input", "value": random.choice(invalid_emails)},
    {"name": "telefon", "type": "input", "value": random.choice(invalid_phones)},
    {"name": "honnan", "type": "select", "value": random.randint(1, 4)},
]

minimal_values = [
    {"name": "name", "type": "input", "value": "Ur"},
    {"name": "email", "type": "input", "value": valid_emails[0]},
    {"name": "telefon", "type": "input", "value": "123"},
    {"name": "honnan", "type": "select", "value": 1},
]

out_minimal_values = [
    {"name": "name", "type": "input", "value": invalid_names[1]},
    {"name": "email", "type": "input", "value": invalid_emails[1]},
    {"name": "telefon", "type": "input", "value": invalid_phones[1]},
    {"name": "honnan", "type": "select", "value": 0},
]

maximum_values = [
    {"name": "name", "type": "input", "value": f"{'Akf12' * 20}"},
    {"name": "email", "type": "input", "value": valid_emails[1]},
    {
        "name": "telefon",
        "type": "input",
        "value": "77036853027244927701715367945591407719403384149830"
    },
    {"name": "honnan", "type": "select", "value": random.randint(1, 4)},
]

out_maximum_values = [
    {"name": "name", "type": "input", "value": invalid_names[2]},
    {"name": "email", "type": "input", "value": valid_emails[1]},
    {
        "name": "telefon",
        "type": "input",
        "value": invalid_phones[2]
    },
    {"name": "honnan", "type": "select", "value": 0},
]

print(random)