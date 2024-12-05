import pyodbc

class DatabaseHandler:
    def __init__(self, connection_string):
        """
        Inicializa la conexión con SQL Server.
        :param connection_string: Cadena de conexión a SQL Server.
        """
        self.connection_string = connection_string
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        """Conecta a la base de datos SQL Server."""
        try:
            conn = pyodbc.connect(self.connection_string)
            print("Conexión a SQL Server establecida.")
            return conn
        except Exception as e:
            print(f"Error al conectar a SQL Server: {e}")
            return None

    def is_file_processed(self, file_hash):
        """Verifica si el archivo ya fue procesado usando su hash."""
        query = "SELECT COUNT(*) FROM ProcessedFiles WHERE FileHash = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (file_hash,))
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Error al consultar el archivo procesado: {e}")
            return False

    def save_processed_file(self, file_hash, file_name):
        """Registra un archivo como procesado en la base de datos."""
        query = "INSERT INTO ProcessedFiles (FileHash, FileName) VALUES (?, ?)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (file_hash, file_name))
            self.connection.commit()
            print(f"Archivo registrado en la base de datos: {file_name}")
        except Exception as e:
            print(f"Error al registrar el archivo: {e}")