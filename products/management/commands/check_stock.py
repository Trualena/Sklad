from django.core.management.base import BaseCommand
from products.utils import check_low_stock

class Command(BaseCommand):
    help = 'Проверяет остатки товаров и создаёт уведомления'

    def handle(self, *args, **options):
        check_low_stock()
        self.stdout.write(self.style.SUCCESS('Проверка остатков выполнена')) 