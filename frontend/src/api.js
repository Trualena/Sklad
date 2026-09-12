//настройка HTTP-клиента
import axios from 'axios';//для преобразования джсон 
const API_BASE_URL = 'http://127.0.0.1:8000/api'; //адрес Django-сервера в режиме разработки 
const api = axios.create({//создание настроенного экземпляра (копия Axios с предустановками) 
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',},//указание что данные отправляются в формате джсон 
});
export default api;