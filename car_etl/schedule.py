from django.conf import settings
from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from .service import LoadDataCAR
from datetime import datetime
from typing import List, Dict, Union

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Task

logger = settings.LOGGER


task_load_car_id='task_load_car'
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.start()

def scheduler_info():
    job = scheduler.get_job(task_load_car_id)
    next_run = job.next_run_time
    now = datetime.now(next_run.tzinfo)
    time_remaining = next_run - now
    return next_run, time_remaining


def task_load_car() -> str:
    """
    Executa a tarefa de carregar os dados do CAR.

    Returns:
        str: Status da execução da tarefa.
    """
    try:
        load_data_car_task = LoadDataCAR()
        status = load_data_car_task.write_atomic() # schedule_simule
        print(f"--------------------- {status} -----------------------")
    except Exception as e:
        logger.error(f"Erro ao processar a tarefa de carga de dados do CAR: {str(e)}")


    

def schedule_task(days_of_week: str, frequency: str, time_of_day: str) -> str:
    """
    Agenda ou modifica a tarefa de carga de dados com base nos parâmetros fornecidos.

    Args:
        days_of_week (str): Dias da semana para execução da tarefa (ex: 'mon,tue,wed').
        frequency (str): Frequência de execução ('daily', 'weekly', 'biweekly', 'monthly').
        time_of_day (str): Horário de execução (formato 'HH:MM').

    Returns:
        str: Mensagem informando a próxima execução agendada.

    Raises:
        HTTPException: Se o formato do horário ou frequência for inválido.
    
    """
    try:
        # Definindo dias padrão para a frequência diária
        if days_of_week.lower() == 'daily':
            days_of_week = 'mon,tue,wed,thu,fri,sat,sun'

        # Extraindo horas e minutos do parâmetro time_of_day
        hour, minute = map(int, time_of_day.split(":"))

        # Definindo o trigger com base na frequência
        if frequency == "weekly":
            trigger = CronTrigger(day_of_week=days_of_week, hour=hour, minute=minute)
        elif frequency == "biweekly":
            trigger = CronTrigger(day_of_week=days_of_week, hour=hour, minute=minute, week='*/2')
        elif frequency == "monthly":
            trigger = CronTrigger(day=1, hour=hour, minute=minute)
        else:
            raise HttpResponse("Entrada de parâmetros inválida.", status=400)

        if scheduler.get_job(task_load_car_id):
            scheduler.remove_job(task_load_car_id)

        scheduler.add_job(task_load_car, trigger=trigger, id=task_load_car_id, max_instances=1, replace_existing=True)

        next_run, time_remaining = scheduler_info()
        str_return = f"Data atual: {datetime.now(next_run.tzinfo).strftime('%d/%m/%Y %H:%M:%S')}, Próxima atualização programada para: {next_run.strftime('%d/%m/%Y %H:%M:%S')}. Tempo restante: {str(time_remaining)}"
        logger.info(str_return)
        if not Task.objects.filter(task_id=task_load_car_id).exists():
            task = Task.objects.create(task_id=task_load_car_id, next_schedule=next_run, time_next_schedule=time_remaining)
        else:
            task = Task.objects.get(task_id=task_load_car_id)
            task.next_schedule=next_run
            task.time_next_schedule=time_remaining
            task.save()
        return str_return

    except ValueError:
        raise HttpResponse("Formato de horário inválido.", status=400)
    except Exception as e:
        logger.error(f"Erro ao agendar tarefa: {str(e)}")
        raise HttpResponse("Erro ao agendar a tarefa.", status=500)

