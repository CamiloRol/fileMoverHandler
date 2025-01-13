from file_mover import FileMoverHandler
from DataBaseHandler import DatabaseHandler
import os

class Main:
    def _init_(self, source_folder, dest_folder):
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.dbHandler = DatabaseHandler(sql_server, db_name, sql_user, sql_password, backup_path, compression_path)
        self.file_mover = FileMoverHandler(self.source_folder, self.dest_folder, self.dbHandler)
        

    def generar_y_comprimir_respaldo(self):
        """Genera y comprime el respaldo antes de mover archivos."""
        respaldo = self.DatabaseHandler.generar_respaldo()
        if respaldo:
            comprimido = self.DatabaseHandler.comprimir_respaldo(respaldo)
            if comprimido:
                print(f"Respaldo comprimido listo en: {comprimido}")
            else:
                print("Error al comprimir el respaldo.")
        else:
            print("Error al generar el respaldo.")

    def move_existing_files(self):
        self.generar_y_comprimir_respaldo()
        print(f"Verificando archivos existentes en {self.source_folder}...")
        for file_name in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.xml'):
                file_hash = self.file_mover.get_file_hash(file_path)
                if not self.dbHandler.is_file_processed(file_hash):
                    self.file_mover.move_file(file_path, file_hash)

if __name__== "_main_":
    source_folder = "C:\\backupsSQL\\zipped"
    dest_folder = "Z:\\"
    sql_server="192.168.0.189",
    db_name="BackUpsDB",
    sql_user="backUpTest",
    sql_password="0L1m4c.12*",
    backup_path="C:\\backupsSQL",
    compression_path="C:\\backupsSQL\\zipped"

    backupHandler = DatabaseHandler(sql_server, db_name, sql_user, sql_password, backup_path, compression_path)


    respaldo = DatabaseHandler.generar_respaldo()
    if respaldo:
        comprimido = DatabaseHandler.comprimir_respaldo(respaldo)
        if comprimido:
            FileMoverHandler.move_file(comprimido)

    main_program = Main(source_folder, dest_folder)
