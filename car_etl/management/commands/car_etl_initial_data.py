from django.core.management.base import BaseCommand
from django.conf import settings

logger = settings.LOGGER

class Command(BaseCommand):
    help = 'Importa dados projeto.'

    def handle(self, *args, **kwargs):
        
        logger.info("Inicializar schedule de agendamento de atualização.")
        self.stdout.write(self.style.SUCCESS('Inicializar schedule de agendamento de atualização.'))
        from ...schedule import schedule_task
        from ...data_acess import return_status_task
        # days_of_week = "sat"
        # frequency = "weekly"
        # time_of_day = "22:00"
        days_of_week, frequency, time_of_day = (s.strip() for s in settings.DEFAULT_SCHEDULE.split(','))
        try:
            schedule_task(days_of_week=days_of_week, frequency=frequency, time_of_day=time_of_day)
            return_status_task()
            self.stdout.write(self.style.SUCCESS(f"Agendamento de atualização dos dados do CAR: {frequency} on {days_of_week} at {time_of_day}."))
            logger.info(f"Agendamento de atualização dos dados do CAR: {frequency} on {days_of_week} at {time_of_day}.")
        except Exception as e:
            logger.error(f"Erro ao inicializar o agendamento da tarefa: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Erro ao inicializar o agendamento da tarefa: {str(e)}"))
            