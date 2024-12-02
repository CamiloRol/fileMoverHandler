import shutil
import hashlib
import paramiko

class FileMoverHandler:
    def __init__(self, source_folder, dest_folder):
        """
        Constructor de la clase. Inicializa las carpetas de origen y destino.
        :param source_folder: Ruta de la carpeta origen.
        :param dest_folder: Ruta de la carpeta destino.
        """
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.processed_files = set()  # Conjunto para almacenar los archivos procesados (por hash)

    def on_created(self, event):
        """
        Método que se ejecuta cuando un nuevo archivo es creado en la carpeta de origen.
        :param event: Evento que contiene la información sobre el archivo.
        """
        print(f"Evento de archivo creado detectado: {event.src_path}") 
        if event.is_directory or not event.src_path.endswith('.xml'):
            return  # Ignorar directorios o archivos que no son .xml

        if not self.is_processed(event.src_path):
            self.move_file(event.src_path)

    def is_processed(self, file_path):
        """
        Verifica si el archivo ya ha sido procesado utilizando su hash.
        :param file_path: Ruta del archivo a verificar.
        :return: True si el archivo ya ha sido procesado, False de lo contrario.
        """
        file_hash = self.get_file_hash(file_path)
        if file_hash in self.processed_files:
            return True
        self.processed_files.add(file_hash)
        return False

    def get_file_hash(self, file_path):
        """
        Calcula el hash MD5 del archivo para verificar si es nuevo o repetido.
        :param file_path: Ruta del archivo a procesar.
        :return: El hash MD5 del archivo.
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def move_file(self, file_path):
        """
        Copia el archivo desde la carpeta de origen a la carpeta de destino.
        :param file_path: Ruta del archivo a mover.
        """
        try:
            print(f"Intentando mover el archivo: {file_path}")
            shutil.copy(file_path, self.dest_folder)
            print(f"Archivo '{file_path}' movido correctamente a {self.dest_folder}.")
        except Exception as e:
            print(f"Error al mover el archivo '{file_path}': {e}")
