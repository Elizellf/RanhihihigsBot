# Файл для хранения секретов

import os
from dotenv import load_dotenv

# предварительно создаем файл .env и помещаем туда Токен
load_dotenv()

# переменные окружения для проекта
TOKEN: str = os.getenv('TOKEN')
