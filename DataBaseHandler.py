import os
import pyodbc
import datetime

class DataBaseHandler:
    def __init__(self, sql_server, db_name, sql_user, sql_password, backup_path):
        self.sql_server = sql_server
        self.db_name = db_name
        self.sql_user = sql_user
        self.sql_password = sql_password
        self.backup_path = backup_path

    def conectar_bd(self):
        """Verifica la conexión a la base de datos."""
        try:
            print("Intentando conectar al servidor SQL...")
            conexion = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.sql_server};UID={self.sql_user};PWD={self.sql_password}"
            )
            print("Conexión exitosa al servidor SQL.")
            return conexion
        except pyodbc.Error as e:
            print(f"Error al conectar con el servidor SQL: {e}")
            return None
    
    def generar_respaldo(self, conexion):
        """Genera el respaldo de la base de datos y lo guarda en la carpeta especificada."""
        try:
            os.makedirs(self.backup_path, exist_ok=True)
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            archivo_respaldo = os.path.join(self.backup_path, f"{self.db_name}_{fecha_actual}.bak")

            print(f"Generando respaldo en: {archivo_respaldo}")
            comando = f"""
            BACKUP DATABASE [{self.db_name}]
            TO DISK = '{archivo_respaldo}'
            WITH FORMAT, INIT,
            NAME = 'Respaldo Diario {fecha_actual}',
            STATS = 10;
            """
            print(f"Ejecutando comando SQL:\n{comando}")
            cursor = conexion.cursor()
            cursor.execute(comando)
            cursor.commit()

            if os.path.exists(archivo_respaldo):
                print(f"Respaldo generado exitosamente: {archivo_respaldo}")
                return archivo_respaldo
            else:
                print(f"Error: El archivo de respaldo no se generó en {archivo_respaldo}.")
                return None
        except pyodbc.Error as sql_error:
            print(f"Error de SQL al generar respaldo: {sql_error}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None