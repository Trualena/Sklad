//Фронтенд. Окно списка уведомлений 
import { useState, useEffect } from 'react';//библиотеки для хранения данных внутри компонента 
import api from '../api';//бэк 

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);//для загрузки [переменная, функция]

  useEffect(() => {//действия при первой загрузке 
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/notifications/');//выполнение запроса на обновление 
      setNotifications(response.data);
    } catch (error) {
      console.error(error);//выводит сообщение об ошибке в консоль 
    } finally {//индикатор загрузки setLoading(false)
      setLoading(false);
    }
  };

  const markAsRead = async (id) => {//асинхранная функция
    try {await api.patch(`/notifications/${id}/`, { is_read: true });//PATCH обновляет только те поля, которые передали
      fetchNotifications();
    } catch (error) {console.error(error);
    }
  };
  if (loading) return <div className="loading">Загрузка...</div>;

  return (
    <>
      <div className="page-header">
        <h1>Уведомления</h1>
      </div>
      {notifications.length === 0 ? (
        <div className="loading">Нет уведомлений</div>
      ) : (
        <div className="notification-list">
          {notifications.map((n) => (
            <div
              key={n.id}
              className={`notification-item ${n.is_read ? 'read' : ''}`}
              onClick={() => !n.is_read && markAsRead(n.id)}
              style={{ cursor: 'pointer' }}
            >
              <div>
                <div className="notification-text">{n.text}</div>
                <div className="notification-time">{n.created_at}</div>
              </div>
              <div className={`notification-status ${!n.is_read ? 'unread' : ''}`}>
                {n.is_read ? 'Прочитано' : 'Новое'}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

export default Notifications;