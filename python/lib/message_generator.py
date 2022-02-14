from models import DB

next_step = {
    "start": "load-excel",
    "load-excel": "data-preprocessing",
    "data-preprocessing": "bill-calc",
    "bill-calc": "normal-analysis",
    "normal-analysis": "mean-analysis",
    "mean-analysis": "similarity-analysis",
    "similarity-analysis": "end"
}

step_to_kor = {
    "start": "시작",
    "load-excel": "엑셀 읽기",
    "data-preprocessing": "데이터 전처리",
    "bill-calc": "청구서 계산",
    "normal-analysis": "일반 분석",
    "mean-analysis": "평균 분석",
    "similarity-analysis": "유사도 분석",
    "end": "종료"
}


class message_generator:
    def __init__(self, id, step):
        self.id = id
        self.db = DB()
        result = self.db.find_process(self.id)
        self.title = result['title']

        self.curr_step = step_to_kor[step]
        self.next_step = step_to_kor[next_step[step]]

    @property
    def success(self):
        msg = "\"{}\"의 {} 작업이 완료 됐습니다. {} 작업을 시작합니다.".format(
            self.title, self.curr_step, self.next_step)
        return msg
