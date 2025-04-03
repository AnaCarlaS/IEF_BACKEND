from django.conf import settings
from django.db import connection
from .models import Task
from .schemas import TaskSchema
logger = settings.LOGGER

def get_scheduler():
    from .schedule import scheduler_info, task_load_car_id
    return scheduler_info, task_load_car_id

def is_running():
    _, task_load_car_id = get_scheduler()
    task = Task.objects.get(task_id=task_load_car_id)
    return task.is_running

def return_status_task():
    scheduler_info, task_load_car_id = get_scheduler()
    next_run, time_remaining = scheduler_info()
    if not Task.objects.filter(task_id=task_load_car_id).exists():
        task = Task.objects.create(task_id=task_load_car_id, next_schedule=next_run, time_next_schedule=time_remaining)
    else:
        task = Task.objects.get(task_id=task_load_car_id)
        task.is_running = False
        task.cancel_requested = False
        task.next_schedule=next_run
        task.time_next_schedule=time_remaining
        task.save()

def set_cancel_process():
    
    _, task_load_car_id = get_scheduler()
    task = Task.objects.get(task_id=task_load_car_id)
    if not task.is_running:
        logger.info('Não há atualizações sendo processadas para serem canceladas.')
        return 'Não há atualizações sendo processadas para serem canceladas.'
    
    task.cancel_requested = True
    task.save()
    
    logger.info('Solicitação de cancelamento da tarefa de atualização das tabelas.')
    return "Processo de atualização das tabelas não foi concluido por cancelamento do usuário."


def get_process_status():
    """
    Obtém o status do processo de carga de dados do CAR e informações sobre as tabelas do banco de dados.
    """
    scheduler_info, task_load_car_id = get_scheduler()
    next_run, time_remaining = scheduler_info()
    task = Task.objects.get(task_id=task_load_car_id)
    task.next_schedule=next_run
    task.time_next_schedule=time_remaining
    task.save()
    tasks = Task.objects.all()
    task_data = [TaskSchema.from_orm(task) for task in tasks]
    query = """
        SELECT
            relname AS table_name,
            pg_size_pretty(pg_total_relation_size(relid)) AS size,
            n_live_tup AS estimated_records
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        AND relname LIKE 'car_etl_%';
    """

    # Executando a consulta com o Django
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    
    tables_info = [
        {
            "tabela": row[0],
            "tamanho": row[1],
            "registros_estimados": row[2]
        }
        for row in result
    ]
    return {'task_info': task_data, 'table_info': tables_info}
