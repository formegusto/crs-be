import pandas as pd
from utils.update_process import update_process
from common import file_name
import os


def load_excel(filepath):
    print("load_excel func ,pid: {}, filename: {}".format(os.getpid(), file_name))
    xlsx = pd.read_excel("static/" + filepath, header=None,
                         skiprows=2, engine="openpyxl")

    return xlsx
