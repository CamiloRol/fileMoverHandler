import os
import zipfile
import shutil

class FileMover:
    def __init__(self, compression_path, final_path):
        self.compression_path = compression_path
        self.final_path = final_path

    """def comprimir_respaldo(self, ruta_respaldo):
        Comprime el archivo de respaldo y lo guarda en la carpeta de compresión.
        try:
            os.makedirs(self.compression_path, exist_ok=True)
            nombre_respaldo = os.path.basename(ruta_respaldo)
            archivo_comprimido = os.path.join(self.compression_path, f"{os.path.splitext(nombre_respaldo)[0]}.zip")
            print(f"Comprimiendo archivo: {ruta_respaldo}")

            with zipfile.ZipFile(archivo_comprimido, 'w') as zipf:
                zipf.write(ruta_respaldo, os.path.basename(ruta_respaldo))
            print(f"Archivo comprimido generado: {archivo_comprimido}")
            return archivo_comprimido
        except Exception as e:
            print(f"Error al comprimir archivo: {e}")
            return None """

    """ def mover_archivo(self, archivo_comprimido):
        Mueve el archivo comprimido a la carpeta final.
        try:
            os.makedirs(self.final_path, exist_ok=True)
            destino = os.path.join(self.final_path, os.path.basename(archivo_comprimido))
            print(f"Moviendo archivo: {archivo_comprimido} -> {destino}")
            shutil.move(archivo_comprimido, destino)
            print("Archivo movido exitosamente.")
        except Exception as e:
            print(f"Error al mover archivo: {e}") """
