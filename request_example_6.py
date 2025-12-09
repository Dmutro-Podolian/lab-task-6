import logging

class FileNotFound(OSError):
    """Exception raised when a file is not found."""

class FileCorrupted(OSError):
    """Exception raised when a file is corrupted."""

def logger(exeption, mode):
    """Decorator for logging exceptions to console or file."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)

            logger.setLevel(logging.ERROR)
            logger.handlers.clear()

            if mode == "console":
                handler = logging.StreamHandler()
            elif mode == "file":
                handler = logging.FileHandler("log.txt", encoding="utf-8")
            else:
                raise ValueError("Невідомий режим логування")
        
            format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            handler.setFormatter(format)
            logger.addHandler(handler)

            try:
                return func(*args, **kwargs)
            except exeption as i:
                logger.error(f"Помилка: {i}")
                raise  
        
        return wrapper
    return decorator

class CSVFileEditor:
    """Class for editing CSV files."""
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name

    @logger(FileCorrupted, mode="file")
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = [line.strip().split(";") for line in file.readlines()]
                return data 
        except Exception:
             raise FileCorrupted("Не вдалося прочитати файл")
        
    @logger(FileCorrupted, mode="file")
    def rewrite(self, rows: list):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                for row in rows:
                    file.write(";".join(row) + "\n")
        except Exception:
            raise FileCorrupted("Не вдалося записати файл")

    @logger(FileCorrupted, mode="file")
    def append_row(self, row: list):
        try:
            with open(self.path, "a", encoding="utf-8") as file:
                    file.write(";".join(row) + "\n")
        except Exception:
            raise FileCorrupted("Не вдалося додати до файлу")
        
csv_file = CSVFileEditor("csv.csv", "csv.scv")

if __name__ == "__main__":
    """Main program for user interaction."""
    while True:
        print("Меню:")
        print("Щоб прочитати файл введіть 1")
        print("Щоб записати файл введіть 2")
        print("Щоб редагувати файл введіть 3")
        action = input("Що бажаєте зробити?")

        if action == "1":
            exel = csv_file.read()
            for row in exel:
                print("\t | \t".join(row))
            
            input()

        elif action == "2":
            rows = []
            print("Введіть значення через ; без пропусків")
            
            while True:
                new_row = input(">>")
                if new_row == "":
                    break
                rows.append(new_row.split(";"))
            
            csv_file.rewrite(rows)

        elif action == "3":
            print("Введіть значення через ; без пропусків")
            while True:
                new_row = input(">>")
                if new_row == "":
                    break
                csv_file.append_row(new_row.split(";"))

            input()
        
        else:
            break

        
