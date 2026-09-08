import { useState } from 'react';
import api from '../api';

function PhotoUpload() {
  const [productId, setProductId] = useState('');
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {//
    e.preventDefault();
    if (!productId || !file) {
      setMessage('Заполните все поля');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);
    if (description) {
      formData.append('description', description);
    }

    try {
      const response = await api.post(
        `/products/${productId}/upload-photo/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setMessage(`Фото успешно загружено! ID: ${response.data.id}`);
      setFile(null);
      setDescription('');
    } catch (error) {
      setMessage('Ошибка загрузки фото');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="photo-upload">
      <h2>Загрузка фото товара</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>ID товара</label>
          <input
            type="number"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Фото</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </div>
        <div className="form-group">
          <label>Описание (опционально)</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Загрузка...' : 'Загрузить фото'}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default PhotoUpload;