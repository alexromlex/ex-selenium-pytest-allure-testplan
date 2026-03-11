from dotenv import load_dotenv
import os


load_dotenv()

valid_login_data = {"username": os.getenv('JWT_USERNAME'), "password": os.getenv('JWT_PASSWORD')}

invalid_login_data = [
    {"username": valid_login_data["username"], "password": "2324234"},
    {"username": "aduyyt", "password": valid_login_data["password"]},
    {"username": "asdasdas", "password": "as1111sd"},
    {"username": "", "password": ""},
    {"username": valid_login_data["username"], "password": ""},
    {"username": "", "password": valid_login_data["password"]},
    {"username": "<script>alert(1)</script>", "password": valid_login_data["password"]},
    {"username": "admin'--", "password": "anything"},
]