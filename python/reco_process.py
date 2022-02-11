from utils import *
import sys
import json


def start():
    return


step_process = [start, load_excel, data_preprocessing, bill_calc,
                normal_analysis, mean_analysis, similarity_analysis]
step_names = ['start', 'load-excel', 'data-preprocessing', 'bill-calc',
              'normal-analysis', 'mean-analysis', 'similarity-analysis']
step_db_save = [False, False, True, False, False, True, True]


class reco_process:
    def __init__(self, min_per, max_per, file_name, id):
        self.min_per = int(min_per)
        self.max_per = int(max_per)
        self.id = id
        self.file_name = file_name
        self.fn = dict()

        for idx, sp in enumerate(step_process):
            sn = step_names[idx]
            ds = step_db_save[idx]
            self.fn[sn] = update_process(sn, id, ds)(sp)


if __name__ == "__main__":
    argv = json.loads(sys.argv[1])

    rp = reco_process(argv['min_per'], argv['max_per'],
                      argv['file_name'], argv['id'])

    step = step_names.copy()
    rp.fn[step[0]]()

    xlsx = rp.fn[step[1]](rp.file_name)

    p, m, d = rp.fn[step[2]](xlsx, db_processing=True)

    bc_result = rp.fn[step[3]](m, p, rp.min_per, rp.max_per)

    na_result = rp.fn[step[4]](bc_result)

    mean_result = rp.fn[step[5]](
        m, p, rp.min_per, rp.max_per, db_processing=True)

    anal_result = rp.fn[step[6]](
        m, p, rp.min_per, rp.max_per, db_processing=True)
