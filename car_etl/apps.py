# from django.apps import AppConfig


# class CarEtlConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "car_etl"


from django.apps import AppConfig
from django.conf import settings
import time

logger = settings.LOGGER

class CarEtlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_etl"
    
    def ready(self):
        logger.info("Inicializar schedule de agendamento de atualização.")
        from .schedule import schedule_task
        from .data_acess import return_status_task
        # days_of_week = "sat"
        # frequency = "weekly"
        # time_of_day = "22:00"
        days_of_week, frequency, time_of_day = (s.strip() for s in settings.DEFAULT_SCHEDULE.split(','))
        try:
            schedule_task(days_of_week=days_of_week, frequency=frequency, time_of_day=time_of_day)
            return_status_task()
            logger.info(f"Agendamento de atualização dos dados do CAR: {frequency} on {days_of_week} at {time_of_day}.")
        except Exception as e:
            logger.error(f"Erro ao inicializar o agendamento da tarefa: {str(e)}")
