import requests as req
import os
from models import DB

db = DB()


def update_process(type, id):
    def decorator(func):
        def wrap(*args, **kwargs):
            print("pid: {} / type: {} / id: {}".format(os.getpid(), type, id))
            db.process_step_update(id, type)

            api_server = "http://localhost:8080"
            update_path = "/process"
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
                "id": id,
                "step": type,
                "type": "change step",
                "status": True
            })

            return result
        return wrap
    return decorator
