from file_mover import FileMoverHandler
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Main:
    def __init__(self, source_folder, dest_folder):
        self.source_folder = source_folder
        self.dest_folder = dest_folder
        self.file_mover = FileMoverHandler(self.source_folder, self.dest_folder)

    def move_existing_files(self):
        print(f"Verificando archivos existentes en {self.source_folder}...")
        for file_name in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, file_name)
            if os.path.isfile(file_path) and file_path.endswith('.xml'):
                print(f"Moviendo archivo existente: {file_path}")
                self.file_mover.move_file(file_path)

    def start_monitoring(self):
        self.move_existing_files()

        event_handler = FileSystemEventHandler()
        event_handler.on_created = self.file_mover.on_created
        
        observer = Observer()
        observer.schedule(event_handler, self.source_folder, recursive=False)
        
        try:
            print(f"Monitoreando la carpeta {self.source_folder}...")
            observer.start()
            while True:
                time.sleep(1)  # Esperar un segundo entre cada iteración
        except KeyboardInterrupt:
            observer.stop()
        finally:
            observer.join()

if __name__ == "__main__":
    source_folder = "C:\\Users\\User\\Desktop\\baseFiles"  
    dest_folder = "C:\\Users\\User\\Desktop\\movingFiles"
    
    main_program = Main(source_folder, dest_folder)
    main_program.start_monitoring()
