from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'fetchAndMailNewQuoraQuestions': {
        'task': 'tasks.fetchAndMailNewQuoraQuestions',
        'schedule': timedelta(seconds=60*5)
    },
}

CELERY_TIMEZONE = 'Asia/Calcutta'
