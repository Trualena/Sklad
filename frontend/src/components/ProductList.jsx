import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get('/products/');
      setProducts(response.data);
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Загрузка товаров...</div>;

  return (
    <>
      <div className="page-header">
        <h1>Список товаров</h1>
        <div className="page-actions">
          <Link to="/add" className="btn btn-primary">+ Добавить товар</Link>
        </div>
      </div>

      <div className="product-grid">
        {products.map((product) => (
          <div className="product-card" key={product.id}>
            <div className="product-card-header">
              <div>
                <div className="product-card-title">{product.name}</div>
                <div className="product-card-article">Арт. {product.article}</div>
              </div>
              <div className="product-card-qr">
                {product.qr_code && (
                  <img
                    src={`http://127.0.0.1:8000${product.qr_code}`}
                    alt="QR"
                  />
                )}
              </div>
            </div>
            <div className="product-card-meta">
              <span>📦 {product.quantity} шт.</span>
              <span>📍 {product.location || '—'}</span>
            </div>
            <div className="product-card-actions">
              <Link to={`/edit/${product.id}`} className="btn btn-outline" style={{ padding: '6px 14px' }}>Изменить</Link>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default ProductList;