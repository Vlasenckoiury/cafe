import os
import json
from django.core.management.base import BaseCommand
from back.models import MenuItem


class Command(BaseCommand):
    help = 'Загрузка меню из JSON-файла'

    def handle(self, *args, **options):
        # Определение пути к файлу
        json_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),  # Получаем директорию текущего скрипта
            'menu.json'  # Имя JSON-файла
        )

        # Проверка, существует ли файл
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f"Файл {json_file_path} не найден"))
            return

        # Открытие и загрузка данных из JSON-файла
        with open(json_file_path, encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                MenuItem.objects.get_or_create(name=item["fields"]["name"], price=item["fields"]["price"])
        self.stdout.write(self.style.SUCCESS("Меню загружено!"))
