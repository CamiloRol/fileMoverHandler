import shutil
import hashlib
import paramiko
import time

class FileMoverHandler:
    def __init__(self, source_folder, dest_folder, dbHandler):
        """
        Constructor de la clase. Inicializa las carpetas de origen y destino.
        :param source_folder: Ruta de la carpeta origen.
        :param dest_folder: Ruta de la carpeta destino.
        """
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.dbHandler = dbHandler
        self.processed_files = set()  # Conjunto para almacenar los archivos procesados (por hash)

    def on_created(self, event):
        """
        Método que se ejecuta cuando un nuevo archivo es creado en la carpeta de origen.
        :param event: Evento que contiene la información sobre el archivo.
        """
        print(f"Evento de archivo creado detectado: {event.src_path}") 
        if event.is_directory or not event.src_path.endswith('.xml'):
            return  # Ignorar directorios o archivos que no son .xml
        file_hash = self.get_file_hash(event.src_path)
        if not self.dbHandler.is_file_processed(file_hash):
            self.move_file(event.src_path, file_hash)

    def get_file_hash(self, file_path):
        """
        Calcula el hash MD5 del archivo para verificar si es nuevo o repetido.
        :param file_path: Ruta del archivo a procesar.
        :return: El hash MD5 del archivo.
        """
        for _ in range(3):  # Intentar 3 veces
            try:
                with open(file_path, "rb") as f:
                    hasher = hashlib.md5()
                    for chunk in iter(lambda: f.read(4096), b""):
                        hasher.update(chunk)
                    return hasher.hexdigest()
            except PermissionError:
                print(f"Archivo bloqueado: {file_path}. Reintentando...")
                time.sleep(3)
        print(f"No se pudo acceder al archivo: {file_path}")
        return None

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
