from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
import os
import sys
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

client = TestClient(app)


def request_main(args):
    try:
        robot_request_library = BuiltIn().get_library_instance("RequestsLibrary")
        title = robot_request_library.get_title()
        logger.console(title)
        exit()
        res = client.get("/")
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code)
        logger.console("Success")
        # sys.stdout.write('Success')
        return "Success"
    except HTTPException as e:
        logger.error(e)


def help():
    print(f"Usage {os.path.basename(sys.argv[0])} [go_to_main, help]")


if __name__ == "__main__":
    actions = {"request_main": request_main}
    # logger.console(sys.argv)
    try:
        action = sys.argv[1]
    except IndexError as e:
        logger.error(e)
        action = "help"

    args = sys.argv[2:]
    try:
        actions[action](*args)
    except (KeyError, TypeError) as e:
        logger.error(e)
        help()
