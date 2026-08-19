from django.core.management.base import BaseCommand#свои команды для управления проектом
from products.ml_utils import train_model
class Command(BaseCommand):
    help = 'Обучает ML-модель для прогноза остатков'
    def handle(self, *args, **options):
        model=train_model()
        if model:#если модель была вернута еспешно 
            self.stdout.write(self.style.SUCCESS('Модель успешно обучена и сохранена'))
        else:
            self.stdout.write(self.style.ERROR(' Ошибка при обучении модели'))
