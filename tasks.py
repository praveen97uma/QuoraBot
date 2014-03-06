from celery import Celery

import newQuestionsBot


app = Celery('tasks', broker='amqp://guest@localhost//')
app.config_from_object('celeryconfig')


@app.task
def fetchAndMailNewQuoraQuestions():
    newQuestionsBot.fetchAndMailNewQuestions()
