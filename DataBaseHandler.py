import pyodbc
import datetime
import os
import zipfile

class DatabaseHandler:
    def _init_(self, sql_server, db_name, sql_user, sql_password, backup_path, compression_path):
        self.sql_server = sql_server
        self.db_name = db_name
        self.sql_user = sql_user
        self.sql_password = sql_password
        self.backup_path = backup_path
        self.compression_path = compression_path

    def generar_respaldo(self):
        """Genera un respaldo de la base de datos."""
        try:
            print("Conectando al servidor SQL...")
            conexion = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={self.sql_server};UID={self.sql_user};PWD={self.sql_password}"
            )
            conexion.autocommit = True
            cursor = conexion.cursor()

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
            cursor.execute(comando)
            print("Respaldo generado exitosamente.")
            return archivo_respaldo
        except Exception as e:
            print(f"Error al generar respaldo: {e}")
            return None
        finally:
            try:
                cursor.close()
                conexion.close()
            except Exception:
                pass

    def comprimir_respaldo(self, ruta_respaldo):
        """Comprime el archivo de respaldo."""
        try:
            os.makedirs(self.compression_path, exist_ok=True)
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            archivo_comprimido = os.path.join(self.compression_path, f"{self.db_name}_{fecha_actual}.zip")
            print(f"Comprimiendo archivo: {ruta_respaldo}")

            with zipfile.ZipFile(archivo_comprimido, 'w') as zipf:
                zipf.write(ruta_respaldo, os.path.basename(ruta_respaldo))
            print(f"Archivo comprimido generado: {archivo_comprimido}")
            return archivo_comprimido
        except Exception as e:
            print(f"Error al comprimir archivo: {e}")
            return None