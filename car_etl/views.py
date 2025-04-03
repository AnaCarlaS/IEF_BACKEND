import asyncio
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.http import HttpResponse
from ninja import NinjaAPI
from django.conf import settings

from .schedule import task_load_car, schedule_task
from .data_acess import set_cancel_process, get_process_status, is_running

logger = settings.LOGGER
executor = ThreadPoolExecutor(max_workers=1)

car_etl = NinjaAPI(urls_namespace='car-etl', version='1.0.0')


@car_etl.get("/modify_schedule")
async def modify_schedule(request, days_of_week: str, frequency: str, time_of_day: str):
    """
    Modifica o agendamento da tarefa de carga de dados do CAR.

    Args:
        days_of_week (str): Dias da semana para execução da tarefa (ex: 'mon,tue,wed').
        frequency (str): Frequência de execução ('daily', 'weekly', 'biweekly', 'monthly').
        time_of_day (str): Horário de execução (formato 'HH:MM').

    Returns:
        dict: Mensagem indicando o status da modificação do agendamento.
    
    Exemples:
        Todos os dias da semana, semanalmente, às 22:00 horas
        url/modify_schedule?days_of_week=daily&frequency=weekly&time_of_day=22:00
        Todo sábado, semanalmente, às 22:00 horas
        url/modify_schedule?days_of_week=sat&frequency=weekly&time_of_day=22:00

    """
    try:
        status_response = await asyncio.to_thread(schedule_task, days_of_week, frequency, time_of_day)
        return {"message": status_response}
    except Exception as e:
        logger.error(f"Erro ao modificar agendamento: {str(e)}")
        raise HttpResponse(f"A atualização do agendamento falhou! {str(e)}", status=400)

@car_etl.get("/run_now")
def run_now(request, confirm: str):
    """
    Executa imediatamente a tarefa de carga de dados do CAR.

    Args:
        confirm (str): Confirmação do usuário para executar a tarefa.

    Returns:
        dict: Mensagem indicando o status da execução.
    
    """
    try:
        if not confirm.lower() in ['sim', 'yes']:
            raise HttpResponse("Confirmação inválida. Por favor, forneça 'sim' ou 'yes'.", status=400)
        
        is_running_response = is_running()
        print(is_running_response)
        if is_running_response:
            return JsonResponse({'message': "A tarefa de atualizar as tabelas do CAR já está sendo executada. Cancele a operação ou tente mais tarde."}, status=202)
        
        executor.submit(task_load_car)

        return JsonResponse({'message': 'Tarefa em execução em background'}, status=202)
    
    except Exception as e:
        logger.error(f"Erro ao executar a tarefa agora: {str(e)}")
        raise HttpResponse(f"A atualização dos dados do CAR falhou! {str(e)}", status=500)


@car_etl.get("/cancel_process")
async def cancel_process(request, confirm: str):
    """
    Cancela o processo de carga de dados em execução.

    Args:
        confirm (str): Confirmação do usuário para cancelar o processo.

    Returns:
        dict: Mensagem indicando o status do cancelamento.
    
    Exemple:
        url_base/car-etl/cancel_process?confirm=yes
    
    """
    try:
        if not confirm.lower() in ['sim', 'yes']:
            raise HttpResponse("Confirmação inválida. Por favor, forneça 'sim' ou 'yes'.", status=400)
        
        status_response = await asyncio.to_thread(set_cancel_process)
        return {"message": status_response}
    except Exception as e:
        logger.error(f"Erro ao cancelar o processo: {str(e)}")
        raise HttpResponse("Cancelamento do processo falhou! {str(e)}", status=500)


@car_etl.get("/process_status")
async def process_status(request):
    """
    Obtém o status atual do processo de carga de dados do CAR.

    Returns:
        JSONResponse: Resposta com as informações do status do processo.
    
    """
    try:
        status_response = await asyncio.to_thread(get_process_status)
        return status_response
    except Exception as e:
        logger.error(f"Erro ao obter status do processo: {str(e)}")
        raise HttpResponse(f"A busca de status de processamento falhou! {str(e)}", status=500)
