from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver #для создания обработчика сигнала из функции 
from .models import Products, History
@receiver (post_save, sender=Products)
def log_product_changes(sender, #регистрация изменений 
                        instance, #объект который был изменен (товар) 
                        created, #был объект уже созданили нет 
                        **kwargs): #доп параметры 
    '''#если товар создан впервые (значение из сигнала)'''
    if created:
        History.objects.create(
            product=instance, #привязка записи к текущему товару 
            action_type='создан',
            details=f'Создан товар: {instance.name} (арт. {instance.article})'
        )
    else: #если created = False
        History.objects.create(
            product=instance,
            action_type='updated',
            details=f'Обновлены данные товара: {instance.name}')

'''удаление'''
@receiver (post_delete, sender=Products)
def log_product_deletion(sender, instance, **kwargs): 
    History.objects.create(
        product=instance,   # запись останется если товар удалён
        action_type='deleted',
        details=f'Удалён товар: {instance.name} (арт. {instance.article})'
    )