from celery_app.celery_work import celery


@celery.task(name="create_task")
def create_task(a, b, c):
    import time

    time.sleep(a)
    return b + c
