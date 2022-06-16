from fastapi.testclient import TestClient
from main import app
from attrs import define
import sys
import os
# from configuration.configuration import Configuration
# from enums.runmode import RunMode
# from persistences.sqlalchemy_engine import init_db_engine
from pprint import pprint

client = TestClient(app)

@define
class User:
    email: str
    password: str
    status: str

    @classmethod
    def from_input(cls, email, password, status='Inactive'):
        return cls(
            email=email,
            password=password,
            status=status
        )

@define
class UserDataBase:
    user: User

    @classmethod
    def from_config(cls):
        # args = {
        #     'mode': RunMode.API_SERVICE
        # }
        # c = Configuration.from_options(args).get_config()['api_service']['persistence']
        # pprint(c) 
        # engine = init_db_engine(c)
        return cls(
            
        )
    def create_user(self, email, password):
        try:
            user = User(email, password)
        except ValueError as e:
            return f'Creating user failed: {e}'
        
        return 'SUCCESS'




def create_user(email, password):

    pass

def help():
    print(f"Usage {os.path.basename(sys.argv[0])} [create, login, help]")

if __name__ == '__main__':
    actions = {
        'Create': create_user
    }
    try:
        action = sys.argv[1]
    except IndexError:
        action = 'help'
    args = sys.argv[2:]
    try:
        actions[action](*args)
    except (KeyError, TypeError):
        help()
