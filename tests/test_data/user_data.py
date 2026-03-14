# REGEX for email validation
# https://pdw.ex-parrot.com/Mail-RFC822-Address.html

valid_names = [
    "Ur",                       # min 2
    f"{'A' * 100}",             # max 100
    "Test User",
    "1234", 
    "<script>alert('XSS')</script>"]

invalid_names = [
    '',
    'a',
    f"{'A' * 101}"             # out of max 100
    ]

valid_emails = [
    f'{"g" * 1}@example.ru',    # min 1 symbol before@
    f'{"e" * 64}@maiL.com',     # max 64 symbol before@
    'pisti.papa@mail.hu',
    'Pisti.Papa@mail-com.net']

invalid_emails = [
    '',
    'a@ur',     # minlen 5
    'plainaddress',
    '#@%^%#$@#$@#.com',
    '@example.com',
    'Joe Smith <email@example.com>',
    'email.example.com',
    'email@example@example.com',
    'あいうえお@example.com',
    'email@example.com (Joe Smith)',    # valid by REGEX
    'email@-example.com',               # valid by REGEX
    'email@example..com',
    '”(),:;<>[\]@example.com',
    'just”not”right@example.com',
    'this\ is"really"not\allowed@example.com',
    "<script>alert('XSS')</script>",
    f'{"m" * 95}@mu.gu'   # maxlen 100
]


valid_phones = [
    '1234567890',
    '+79001234567',
    '+36 30 123 4567',
    '123-456-7890',
    '(123) 456-7890',
    '123.456.7890',
    '+1-123-456-7890',
    'tel: +33225445578',
    "<script>alert('125444556')</script>",
    "77036853027244927701715367945591407719403384149830"        # max 50
    ]

invalid_phones = [
    '',
    '12',                                                       # 2 > min 3
    '770368530272449277017153679455914077194033841498301',      # 51 > max 50
    'abc',
    '!@#$%^&*()',
    "<script>alert('XSS')</script>"
    ]
