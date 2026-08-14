'''Для хранения вспомогательных функций: 
1) Настройка уведомлений '''

from .models import Products, Notification
def check_low_stock(): #для создания уведомлений если товара меньше 5 
    low_stock_products=Products.objects.filter(quantity__lt=5)
    for product in low_stock_products:
        #проверка на наличие уведомлений 
        existing=Notification.objects.filter(
            product=product, # уведомление привязано к этому конкретному товару
            is_read=False,#уведомление ещё не прочитано сотрудником
            text__icontains=f'{product.name}').exists()#поиск вне зависимости от регистра
        if not existing:
            Notification.objects.create(product=product, text=f'Товар "{product.name}" (арт. {product.article}) — осталось всего {product.quantity} шт.! Срочно пополните запас!')