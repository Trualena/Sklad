'''Для хранения вспомогательных функций: 
1) Настройка уведомлений '''

from .models import Products, Notification
from .ml_utils import predict_stock


'''
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
'''   
"""заменена редыдущая функция на функцию которая проверяет товары с использованием ML-прогноза.
Если модель предсказывает, что товар закончится через 3 дня то создаёт уведомление."""
def check_low_stock():
    for product in Products.objects.all():
        predicted_quantity = predict_stock(product.id, days_ahead=3)
        if predicted_quantity <= 0:# Если прогноз показывает, что товар закончится через 3 дня
            existing = Notification.objects.filter(#проверяет есть ли непрочитанное уведомление 
                product=product,
                is_read=False,
                text__icontains=f'{product.name}'
            ).exists()

            if not existing:
                Notification.objects.create(
                    product=product,
                    text=f' По прогнозу товар "{product.name}" (арт. {product.article}) закончится через 3 дня! Текущий остаток: {product.quantity} шт. Срочно пополните запас!'
                )

