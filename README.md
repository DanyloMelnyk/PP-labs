# Лабраторна робота №1 з прикладного програмування Мельника Данила
### Варіант 17 (python 3.7.*, venv + requirements.txt)
* Клонувати репозиторій
    ```
    git clone https://github.com/DanyloMelnyk/PP-labs.git
    ``` 

* Створити віртуальне середовище 
    ```
    python -m venv venv
    ``` 
    або 
    ```
    C:/Users/Danylo/AppData/Local/Programs/Python/Python37/python.exe -m venv venv
    ``` 
    якщо в `PATH` немає необхідного інтерпретатора

* Активувати віртуальне середовище 
    ```
    source venv/Scripts/activate
    ```
    або
    ```
    venv\Scripts\activate.bat
    ```    
  
* Встановити залежності проекту 
    ```
    pip install -r requirements.txt
    ```
  
* Запустити WSGI сервер 
    ```
    waitress-serve --listen=*:8000 main:app
    ```
  
* Перевірити роботу
    ```
    http://127.0.0.1:8000/api/v1/hello-world-17
    ```