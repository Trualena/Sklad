import pandas as pd#Работа с таблицами
import numpy as np#Математические операции над массивами
from sklearn.linear_model import LinearRegression# простая модель ML (линейная регрессия), остаток будет предсказываться по дням
import joblib#Сохранение и загрузка обученной модели в файл 
import os#Работа с путями файлов
from datetime import timedelta#Прибавление/вычитание дней из даты
from django.utils import timezone#Получение текущего времени для расчёта за последние 30 дней
from .models import Products, History, Notification
#Путь к файлу модели: 
MODEL_PATH=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                         '..',#поднимается на уровень выше (в папку sklad/) 
                                                         'models', #заходит в папку models/
                                                         'stock_model.pkl'))#имя файла для сохранения модели

'''модель будет один раз при старте сервера загружаться и храниться здесь, 
чтобы не читать файл каждый раз при новом запросе''' 
model=None #используется для кэширования обученной модели в памяти сервера  
'''Загружает модель из файла, если он существует.
Сохраняет её в глобальную переменную _model.
Если файла нет пишет предупреждение.'''
def load_model():
    global model #работ с переменной model=None 
    if os.path.exists(MODEL_PATH):
        model=joblib.load(MODEL_PATH)
        print('Модель успешно загружена')
        return model
    else:
        print("Файл модели не найден или модель не загружена")
        return None

"""Собирает данные из истории для обучения модели.
Для каждого товара считает, сколько штук уходило в день.
Возвращает DataFrame с признаками и целевой переменной."""
def prepare_training_data():
    history_notes=History.objects.filter(action_type__in=['updated', 'created', 'quantity_changed']).order_by('product', 'created_at')# сортирует записи сначала по товару потом по времени
    data=[]#собранные данные 
    for product in Products.objects.all():#анализ истории каждого товара 
        product_history=history_notes.filter(product=product)
        if product_history.count()<3:
            continue#Модели нужно хотя бы 3 точки данных
        product_history=product_history.order_by('created_at')#сортировка по времени 
        current_quntity=product.quantity#текущее количество товара
        # Проходим по записям и собираем изменения
        for i, entry in enumerate(product_history):#перебираtn все записи истории для текущего товара, запоминая их индекс i и саму запись entry 
            if i > 0:#если запись не первая  
                prev_entry = product_history[i - 1]#предыдущая запись 
                days_diff = (entry.created_at - prev_entry.created_at).days#разница в днях 
                if days_diff > 0:#если записи были в разные дни 
                    #пока что реальных данных мало 
                    pass

        # для каждого товара собираем историю изменения количества
        end_date = timezone.now()#текущее время 
        start_date = end_date - timedelta(days=30)#дата 30 дней назад от текущего момента

        # Получаем все изменения количества (из истории)
        # Для простоты будем использовать текущий остаток и дату создания
        # Создадим искусственные данные для обучения

    # Если данных недостаточно нужно брать синтетические данные для демонстрации
    return _generate_synthetic_data()


def _generate_synthetic_data():
    # Создаём датафрейм с днями и остатками
    days = np.arange(1, 31).reshape(-1, 1)  # 30 дней. преобразует одномерный массив в двумерный 
    # пустой список, в который будут собираться данные по каждому товару и каждому дню
    products_data = []
    for product_id in range(1, 6):#модель из 5 товаров 
        initial_quantity = np.random.randint(50, 200)#начальное количество товара на складе (рандом)
        daily_usage = np.random.uniform(1, 10)# случайное число расходования 
        #остаток уменьшается каждый день
        quantities = initial_quantity - daily_usage * days.flatten()#показывающих, сколько товара осталось в каждый из этих дней 
        quantities = np.maximum(quantities, 0)  # заменяет отрицательные значения на 0 
        for i, day in enumerate(days.flatten()):
            products_data.append({
                'product_id': product_id,
                'day': day,
                'quantity': quantities[i]})
    df = pd.DataFrame(products_data)#список словарей в таблице 
    return df


def train_model():
    """Обучает модель линейной регрессии (остаток=скорось расхода*день+начальный остаток)
    Сохраняет модель в файл.
    """
    print("Начинаем обучение модели")
    df = prepare_training_data()
    if df.empty:
        print("Нет данных для обучения")
        return None
    X = df[['day']].values#только колонку day в виде DataFrame с одной колонкой (в виде двумерного массива)
    y = df['quantity'].values

    # Создаём и обучаем модель
    model = LinearRegression()#класс из библиотеки scikit-learn 
    model.fit(X, y)#Модель обучается на данных:
    '''
ищет зависимость: quantity = a * day + b
Находит коэффициенты a (скорость расхода) и b (начальный остаток)
 модель может предсказывать остаток для любого дня
    '''
#сохоанение 
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)#Создаёт папку для сохранения модели, если её нет
    joblib.dump(model, MODEL_PATH)#Сохраняет обученную модель в файл stock_model.pkl
    print(f" Модель сохранена в {MODEL_PATH}")
    return model


def predict_stock(product_id, days_ahead=3):#Предсказывает остаток товара через 3 дня и возвращает предсказанное количество.

    if model is None:
        load_model()#загрузка обученной модели из файла при старте сервера 
#Если после попытки загрузить модель она пуста
    if model is None:
        product = Products.objects.get(id=product_id)
        return max(0, product.quantity - 5 * days_ahead)
    product = Products.objects.get(id=product_id)
    history = History.objects.filter(product=product).order_by('created_at')
    if history.count() < 3:
        return max(0, product.quantity - 5 * days_ahead)
    first_entry = history.first()
    last_entry = history.last()
    days_diff = (last_entry.created_at - first_entry.created_at).days
    if days_diff <= 0:
        return product.quantity#Если разница в днях ≤ 0 не прогнозирует
    #если нет начального количества в истори средний расход = 5 
    daily_usage = 5
    predicted = product.quantity - daily_usage * days_ahead
    return max(0, predicted)

'''проверка товаров с этим модулем '''
def check_stock_with_ml():
    if model is None:
        load_model()
    for product in Products.objects.all():
        predicted_quantity = predict_stock(product.id, days_ahead=3)

        if predicted_quantity <= 0:
            # Проверяем, есть ли уже непрочитанное уведомление
            existing = Notification.objects.filter(
                product=product,
                is_read=False,
                text__icontains=f'{product.name}').exists()

            if not existing:
                #уведомление
                Notification.objects.create(
                    product=product,
                    text=f' По прогнозу товар "{product.name}" (арт. {product.article}) закончится через 3 дня! Текущий остаток: {product.quantity} шт. Срочно пополните запас!'
                )