from DataBaseHandler import DataBaseHandler
from file_mover import FileMover

if __name__ == "__main__":
    # Configuración de respaldo
    sql_server = "192.168.0.189"
    db_name = "BackUpsDB"
    sql_user = "backUpTest"
    sql_password = "0L1m4c.12*"
    backup_path = "C:\\Users\\camilo\\Desktop\\Nueva carpeta"

    # Configuración de carpetas
    compression_path = "C:\\Users\\camilo\\Desktop\\Nueva carpeta"
    final_path = "Z:\\"

    # Instanciar clases
    db_handler = DataBaseHandler(sql_server, db_name, sql_user, sql_password, backup_path)
    file_mover = FileMover(compression_path, final_path)

    # Generar respaldo
    conexion = db_handler.conectar_bd()
    respaldo = db_handler.generar_respaldo(conexion)
    print(f"lo tenemos {respaldo}")
    """ if respaldo:
        # Comprimir respaldo
        comprimido = file_mover.comprimir_respaldo(respaldo)
        if comprimido:
            # Mover archivo comprimido a la carpeta final
            file_mover.mover_archivo(comprimido) """
