import requests as req
import os


def update_process(type, id):
    def decorator(func):
        def wrap(*args, **kwargs):
            print("pid: {} / type: {} / id: {}".format(os.getpid(), type, id))
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
                "type": type,
                "status": True
            })

            return result
        return wrap
    return decorator
