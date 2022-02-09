import requests as req
from common import file_name
import os


def update_process(type):
    def decorator(func):
        def wrap(*args, **kwargs):
            api_server = "http://localhost:8080"
            update_path = "/process"
            print("update_process decorator ,pid: {}, filename: {}".format(
                os.getpid(), file_name))

            # try:
            #     result = func(*args, **kwargs)

            #     req.patch(api_server + update_path, json={
            #         "type": type,
            #         "status": True
            #     })

            #     return result
            # except:
            #     req.patch(api_server + update_path, json={
            #         "type": type,
            #         "status": False
            #     })
            #     return
            result = func(*args, **kwargs)

            req.patch(api_server + update_path, json={
                "type": type,
                "status": True
            })

            return result
        return wrap
    return decorator
