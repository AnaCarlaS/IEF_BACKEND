from pathlib import Path
import zipfile
from itertools import count
from datetime import datetime
import csv
from io import StringIO
import geopandas as gpd
import psycopg
from psycopg import sql
# from shapely import to_wkb, wkb, wkt
from django.conf import settings
# from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction, connection
from django import db
db.reset_queries()

from .models import (
    AreaImovel1, Apps1, Apps2, Apps3, Apps4, Apps5, Apps6, Apps7,
    AreaConsolidada1, AreaConsolidada2, AreaPousio1, Hidrografia1,
    ReservaLegal1, ServidaoAdministrativa1, UsoRestrito1,
    VegetacaoNativa1, VegetacaoNativa2
)

from .models import Task

from .config_database import (
    disable_triggers, enable_triggers, optimize_postgres,
    restore_postgres, list_tables_and_indexes
)

logger = settings.LOGGER

def get_scheduler():
    from .schedule import scheduler_info, task_load_car_id
    return scheduler_info, task_load_car_id


model_mapping = {
    "AREA_IMOVEL_1": AreaImovel1,
    "APPS_1": Apps1,
    "APPS_2": Apps2,
    "APPS_3": Apps3,
    "APPS_4": Apps4,
    "APPS_5": Apps5,
    "APPS_6": Apps6,
    "APPS_7": Apps7,
    "AREA_CONSOLIDADA_1": AreaConsolidada1,
    "AREA_CONSOLIDADA_2": AreaConsolidada2,
    "AREA_POUSIO_1": AreaPousio1,
    "HIDROGRAFIA_1": Hidrografia1,
    "RESERVA_LEGAL_1": ReservaLegal1,
    "SERVIDAO_ADMINISTRATIVA_1": ServidaoAdministrativa1,
    "USO_RESTRITO_1": UsoRestrito1,
    "VEGETACAO_NATIVA_1": VegetacaoNativa1,
    "VEGETACAO_NATIVA_2": VegetacaoNativa2
}

class LoadDataCAR:
    
    def __init__(self) -> None:
        """
        Inicializa a classe `LoadDataCAR`. Carrega a configuração do arquivo `.env` e
        define uma engine e um schema para acessar o banco de dados.
        """
        self.chunk_size = 10000
        self.encoding = "iso-8859-1"
        self.folder_car = Path(settings.FOLDER_CAR)
        self.db_schema = settings.DB_SCHEMA
        self.tema_car = [s.strip() for s in settings.TEMA_CAR.split(',')]
        db_settings = settings.DATABASES['default']
        self.dsn = (
            f"dbname={db_settings['NAME']} "
            f"user={db_settings['USER']} "
            f"password={db_settings['PASSWORD']} "
            f"host={db_settings['HOST']} "
            f"port={db_settings['PORT']}"
        ) 
    
    def write_atomic(self):
        logger.info(f"Início write dados CAR no database.")
        scheduler_info, task_load_car_id = get_scheduler()
        task = Task.objects.get(task_id=task_load_car_id)
        if task.is_running:
            logger.info("A tarefa de atualizar as tabelas do CAR já está sendo executada.")
            return "A tarefa de atualizar as tabelas do CAR já está sendo executada. Cancele a operação ou tente mais tarde."
        
        task.is_running = True
        task.last_started = datetime.now()
        task.save()
        start_total = datetime.now()
        files_shapefile_path = self._validated_files(self.folder_car, self.tema_car)
        list2rename = []
        connection_psycopg = psycopg.connect(self.dsn)
        for name_tema, shapefile_zip_path, shapefiles in files_shapefile_path:
            for shapefile in shapefiles:                
                start_time_shp = datetime.now()
                logger.info(f"----> Tema: {name_tema}, Shapefile: {shapefile}")
                with connection_psycopg.cursor() as cursor_psycopg:
                    try: 
                        optimize_postgres(cursor_psycopg)
                        shp_name = shapefile.split('.')[0]
                        shapefile_path = str(shapefile_zip_path) + '!' + shapefile
                        model_class = model_mapping.get(shp_name)
                        table_name_db = model_class._meta.db_table
                        model_fields = [field.name for field in model_class._meta.get_fields() if field.name != 'gid']
                        temp_table_name_db = f"{table_name_db}_tmp" 
                        list2rename.append((temp_table_name_db, table_name_db))
                        cursor_psycopg.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(self.db_schema, temp_table_name_db)))
                        cursor_psycopg.execute(sql.SQL("CREATE TABLE {} (LIKE {} INCLUDING ALL);").format(sql.Identifier(self.db_schema, temp_table_name_db), sql.Identifier(self.db_schema, table_name_db)))
                        disable_triggers(cursor_psycopg, temp_table_name_db)
                        total_register = 0
                        chunk_number = 1
                        for start in count(0, self.chunk_size):
                            task.refresh_from_db()
                            if task.cancel_requested:
                                logger.info("Interrupção solicitada. Parando a tarefa.")
                                task.is_running = False
                                task.cancel_requested = False
                                task.last_status = "Cancelada"
                                next_run, time_remaining = scheduler_info()
                                task.next_schedule = next_run
                                task.time_next_schedule = time_remaining
                                task.save()
                                restore_postgres(cursor_psycopg)
                                connection_psycopg.commit()
                                connection_psycopg.close()
                                logger.info(f"Cancelamento do usuário, as tabelas temporárias serão deletadas")
                                with connection.cursor() as cursor_context:
                                    for old_name, _ in list2rename:
                                        cursor_context.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(self.db_schema, old_name)))
                                message = "Processo de atualização das tabelas não foi concluido por cancelamento do usuário."
                                logger.info(message)
                                return message
                            start_time = datetime.now()
                            gdf_chunk = gpd.read_file(shapefile_path, encoding=self.encoding, rows=slice(start, start + self.chunk_size))
                            if gdf_chunk.empty:
                                break
                            gdf_chunk['geometry'] = [geom.wkb_hex for geom in gdf_chunk['geometry'].values]
                            gdf_chunk = gdf_chunk[model_fields]
                            args = [list(gdf_chunk[i]) for i in gdf_chunk.columns]
                            args.insert(0, list(start + gdf_chunk.index + 1))
                            data_iter = zip(*args)
                            string_buffer = StringIO()
                            writer = csv.writer(string_buffer)
                            writer.writerows(data_iter)
                            string_buffer.seek(0)
                            sql_copy = sql.SQL('COPY {} FROM STDIN WITH (FORMAT CSV)').format(sql.Identifier(self.db_schema, temp_table_name_db))
                            with string_buffer as buffer: 
                                with cursor_psycopg.copy(sql_copy) as copy:
                                    while data_buffer := buffer.read(self.chunk_size):
                                        copy.write(data_buffer)
                            logger.info(f'--> Chunk {chunk_number}, registros de {total_register} a {total_register + len(gdf_chunk)-1}, tabela {table_name_db}, tempo: {datetime.now() - start_time}.')
                            total_register += len(gdf_chunk) 
                            chunk_number += 1
                            connection_psycopg.commit()
                    except Exception as e:
                        logger.error(f"Erro durante a inserção em massa: {e}")
                        restore_postgres(cursor_psycopg)
                        connection_psycopg.commit()
                        connection_psycopg.close()
                        logger.info("Transação revertida devido a erro.")
                        task.is_running = False
                        task.last_status = "Falha"
                        next_run, time_remaining = scheduler_info()
                        task.next_schedule = next_run
                        task.time_next_schedule = time_remaining
                        task.save()
                        logger.error(f"Erro ao renomear tabelas, as tabelas temporárias serão deletadas: {e}")
                        with connection.cursor() as cursor_context:
                            for old_name, _ in list2rename:
                                cursor_context.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(self.db_schema, old_name)))
                        return f"Erro durante a inserção em massa: {e}"
                    finally:
                        restore_postgres(cursor_psycopg)
                        connection_psycopg.commit()
                        logger.info("Configurações do PostgreSQL restauradas.")
                logger.info(f"FIM WRITE Tema: {name_tema}, Shapefile: {shapefile}, tempo: {datetime.now() - start_time_shp}.")
        
        connection_psycopg.close()
        logger.info(f'Tempo total WRITE: {datetime.now() - start_total}.')
        
        try:
            logger.info(f'Transação atômica para renomear temporária para atualizada.')
            with transaction.atomic():
                with connection.cursor() as cursor_context:
                    for old_name, new_name in list2rename:  # (temp_table_name_db, table_name_db)
                        cursor_context.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(self.db_schema, new_name)))
                        cursor_context.execute(sql.SQL('ALTER TABLE {} RENAME TO {};').format(sql.Identifier(self.db_schema, old_name), sql.Identifier(new_name)))
                        cursor_context.execute(sql.SQL("ANALYZE {};").format(sql.Identifier(self.db_schema, new_name)))
                        enable_triggers(cursor_context, new_name)
        except Exception as e:
            logger.error(f"Erro ao renomear tabelas, as tabelas temporárias serão deletadas: {e}")
            with connection.cursor() as cursor_context:
                for old_name, _ in list2rename:
                    cursor_context.execute(sql.SQL('DROP TABLE IF EXISTS {};').format(sql.Identifier(self.db_schema, old_name)))
            task.is_running = False
            task.last_status = "Falha"
            next_run, time_remaining = scheduler_info()
            task.next_schedule = next_run
            task.time_next_schedule = time_remaining
            task.save()
            return f"Erro ao renomear tabelas: {e}"
        
        list_tables_and_indexes(connection)
        logger.info(f'Tempo total GERAL: {datetime.now() - start_total}.')
        task.is_running = False
        task.last_status = "Sucesso"
        task.last_finished = datetime.now()
        next_run, time_remaining = scheduler_info()
        task.next_schedule = next_run
        task.time_next_schedule = time_remaining
        task.save()
        logger.info("Sucesso")
        return 'Sucesso' 
    
    def _validated_files(self, folder_car: Path, tema_car:list[str]) -> list[str]:
        """
        Extrai os nomes dos shapefiles contidos no arquivo ZIP.

        Args:
            folder_car (Path): Caminho para os arquivos ZIP contendo os shapefiles.
            tema_car list[str]: Lista de nomes dos temas a serem importados vindos do
            arquivo .env.

        Returns:
            list[str]: Lista de nomes dos shapefiles encontrados dentro do arquivo ZIP.
        """
        total_temas = 0
        total_shapefiles = 0
        files_shapefile_path = []
        for name_tema in tema_car:
            shapefile_zip_path = folder_car / f"{name_tema}.zip"
            shapefiles = self._valide_paths_and_zip_file(shapefile_zip_path)
            files_shapefile_path.append((name_tema, shapefile_zip_path, shapefiles))
            total_temas += 1
            total_shapefiles += len(shapefiles)
        
        logger.info(f'Total de temas: {total_temas}, shapefiles totais: {total_shapefiles}.')
        return files_shapefile_path

    def _valide_paths_and_zip_file(self, shapefile_zip_path: Path) -> None:
        """
        Verifica se o caminho definido em .env existe e também a integridade do arquivo ZIP.

        Args:
            shapefile_zip_path (Path): Caminho para o arquivo ZIP contendo os shapefiles.

        Returns:
            None
        """

        if not shapefile_zip_path.parent.exists():
            logger.error(f"O diretório {shapefile_zip_path.parent} não existe. Verifique se o caminho está correto nas variáveis de ambiente.")
            # raise FileNotFoundError(f"O diretório {shapefile_zip_path.parent} não foi encontrado.")
        
        if shapefile_zip_path.exists():
            logger.info(f"Arquivo {shapefile_zip_path} encontrado.")
        else:
            logger.error(f"Arquivo {shapefile_zip_path} não encontrado. Verifique se o arquivo foi baixado corretamente.")
            # raise FileNotFoundError(f"O arquivo {shapefile_zip_path} não foi encontrado.")
        
        try:
            with zipfile.ZipFile(shapefile_zip_path, 'r') as zip_ref:
                
                shapefiles = [name for name in zip_ref.namelist() if name.endswith('.shp')]
                
                if shapefiles:
                    logger.info(f"Arquivo {shapefile_zip_path} está íntegro e contém os shapefiles: {shapefiles}")
                else:
                    logger.error(f"Arquivo {shapefile_zip_path} não contém shapefiles.")
                    raise zipfile.BadZipFile(f"Arquivo {shapefile_zip_path} não contém shapefiles válidos.")
                
                return shapefiles
            
        except zipfile.BadZipFile as e:
            logger.error(f"Erro ao ler arquivo ZIP {shapefile_zip_path}: {e}")
            # raise zipfile.BadZipFile(f"Erro ao ler arquivo ZIP {shapefile_zip_path}: {e}")
    
    
    def schedule_simule(self):
        import time
        logger.info(f"Início: schedule_simule")
        for i in range(5):
            logger.info(f"Processo: {i+1}")
            time.sleep(1)
        logger.info(f"Fim: schedule_simule")
        return "Sucesso"

