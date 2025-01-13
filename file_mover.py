import shutil

class FileMoverHandler:
    def __init__(self, source_folder, dest_folder, dbHandler):
        """
        Constructor de la clase. Inicializa las carpetas de origen y destino.
        :param source_folder: Ruta de la carpeta origen.
        :param dest_folder: Ruta de la carpeta destino.
        """
        self.source_folder = source_folder
        self.dest_folder = "dest_folder"
        self.dbHandler = dbHandler
        self.processed_files = set()  # Conjunto para almacenar los archivos procesados (por hash)

    def move_file(self, file_path, file_hash):
        """
        Copia el archivo desde la carpeta de origen a la carpeta de destino.
        :param file_path: Ruta del archivo a mover.
        """
        try:
            print(f"Intentando mover el archivo: {file_path}")
            shutil.copy(file_path, self.dest_folder)
            file_name = file_path.split("\\")[-1]
            self.dbHandler.save_processed_file(file_hash, file_name)
            print(f"Archivo '{file_path}' movido correctamente a {self.dest_folder}.")
        except Exception as e:
            print(f"Error al mover el archivo '{file_path}': {e}")
