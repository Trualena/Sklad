import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

function ProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    article: '',
    quantity: 0,
    location: '',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (id) {
      fetchProduct();
    }
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await api.get(`/products/${id}/`);
      setFormData(response.data);
    } catch (error) {
      console.error('Ошибка загрузки товара:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (id) {
        await api.put(`/products/${id}/`, formData);
      } else {
        await api.post('/products/', formData);
      }
      navigate('/');
    } catch (error) {
      console.error('Ошибка сохранения:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="product-form">
      <h2>{id ? 'Редактировать товар' : 'Добавить товар'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Название</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Артикул</label>
          <input
            type="text"
            name="article"
            value={formData.article}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Количество</label>
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Местоположение</label>
          <input
            type="text"
            name="location"
            value={formData.location || ''}
            onChange={handleChange}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Сохранение...' : 'Сохранить'}
        </button>
      </form>
    </div>
  );
}

export default ProductForm;