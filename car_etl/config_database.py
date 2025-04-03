from psycopg import sql
from django.conf import settings
logger = settings.LOGGER

def get_indexes_for_table(cursor, table_name):
    """Recupera os nomes dos índices de uma tabela específica."""
    cursor.execute(sql.SQL("SELECT indexname FROM pg_indexes WHERE tablename = {};").format(table_name))
    indexes = cursor.fetchall()
    return [index[0] for index in indexes]


# Função auxiliar para desativar triggers e remover índices
def disable_triggers(cursor, table_name):
    cursor.execute(sql.SQL("ALTER TABLE {} DISABLE TRIGGER ALL;").format(sql.Identifier(table_name)))
    logger.info(f"Triggers desabilitados para a tabela {table_name}.")
    # remover indice cod_imovel
    name_field = 'cod_imovel'
    name_index = f"{table_name}_{name_field}_idx"
    cursor.execute(sql.SQL("DROP INDEX IF EXISTS {};").format(sql.Identifier(name_index)))
    logger.info(f"Índice {name_index} removido.")
    # remover indice espacial geometry
    name_field = 'geometry'
    geometry_index = f"{table_name}_{name_field}_idx"
    cursor.execute(sql.SQL("DROP INDEX IF EXISTS {};").format(sql.Identifier(geometry_index)))
    logger.info(f"Índice {geometry_index} removido.")
    # remover demais indices de forma explicita
    index_names = get_indexes_for_table(cursor, table_name)
    logger.info(index_names)
    for index in index_names:
        #if 'pkey' not in index:  # Evitar remover índice da chave primária
        cursor.execute(sql.SQL("ALTER TABLE {} DROP CONSTRAINT IF EXISTS {};").format(sql.Identifier(table_name), sql.Identifier(index)))
        cursor.execute(sql.SQL("DROP INDEX IF EXISTS {};").format(sql.Identifier(index)))
        logger.info(f"Índice {index} removido.")


# Função auxiliar para reativar triggers e recriar índices
def enable_triggers(cursor, table_name):
    cursor.execute(sql.SQL("ALTER TABLE {} ENABLE TRIGGER ALL;").format(sql.Identifier(table_name)))
    logger.info(f"Triggers habilitados para a tabela {table_name}.")
    # criar indice em pkey
    name_field = 'gid'
    name_index = f"{table_name}_pkey"
    cursor.execute(sql.SQL("ALTER TABLE {} ADD PRIMARY KEY ({});").format(sql.Identifier(table_name), sql.Identifier(name_field)))
    logger.info(f"Índice {name_index} recriado.")
    # criar indice em cod_imovel
    name_field = 'cod_imovel'
    name_index = f"{table_name}_{name_field}_idx"
    cursor.execute(sql.SQL("CREATE INDEX {} ON {} ({});").format(sql.Identifier(name_index), sql.Identifier(table_name), sql.Identifier(name_field)))
    logger.info(f"Índice {name_index} recriado.")
    # criar indice espacial em geometry
    name_field = 'geometry'
    geometry_index = f"{table_name}_{name_field}_idx"
    cursor.execute(sql.SQL("CREATE INDEX {} ON {} USING gist ({});").format(sql.Identifier(geometry_index), sql.Identifier(table_name), sql.Identifier(name_field)))
    logger.info(f"Índice {geometry_index} recriado.")
    logger.info(f"Reindexação da tabela {table_name} concluída.")
    index_names = get_indexes_for_table(cursor, table_name)
    for index in index_names:
        logger.info(f"Índice {index}: existe.")

# Função auxiliar para configurar o PostgreSQL
def optimize_postgres(cursor):
    cursor.execute("SET synchronous_commit TO OFF;")
    cursor.execute("SET work_mem TO '64MB';")
    cursor.execute("SET maintenance_work_mem TO '512MB';")


# Função auxiliar para restaurar as configurações padrão do PostgreSQL
def restore_postgres(cursor):
    cursor.execute("SET synchronous_commit TO ON;")
    cursor.execute("SET work_mem TO '64MB';")
    cursor.execute("SET maintenance_work_mem TO '128MB';")


def list_tables_and_indexes(connection):
    with connection.cursor() as cursor:
        # Consulta as tabelas e seus índices
        cursor.execute("""
            SELECT
                t.tablename,
                i.indexname,
                i.indexdef
            FROM
                pg_indexes i
            JOIN
                pg_tables t ON i.tablename = t.tablename
            WHERE
                t.schemaname = 'public'  -- Considera apenas o schema 'public'
                AND t.tablename LIKE 'car_etl_%'  -- Filtra tabelas que começam com 'car_etl_'
            ORDER BY
                t.tablename, i.indexname;
        """)
        results = cursor.fetchall()
        if results:
            for table, index_name, index_def in results:
                logger.info(f"Tabela: {table}, Índice: {index_name}, Definição: {index_def}")
        else:
            logger.info("Nenhuma tabela ou índice encontrado.")


