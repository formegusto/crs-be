import requests as req
import os
from lib import message_generator
from models import DB

db = DB()


def update_process(step, id, db_save):
    def decorator(func):
        def wrap(*args, **kwargs):
            print("pid: {} / type: {} / id: {}".format(os.getpid(), step, id))
            db.process_step_update(id, step)
            mg = message_generator(id, step)

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

            if db_save:
                in_db = None
                if type(result) == tuple:
                    in_db = result[len(result) - 1]
                else:
                    in_db = result

                db.save_new_process(id, in_db)

            req.patch(api_server + update_path, json={
                "id": id,
                "step": step,
                "type": "process success",
                "status": True,
                "message": mg.success
            })

            return result
        return wrap
    return decorator
