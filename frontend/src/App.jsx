import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import ProductList from './components/ProductList';
import ProductForm from './components/ProductForm';
import PhotoUpload from './components/PhotoUpload';
import Notifications from './components/Notifications';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        {/* Боковое меню */}
        <aside className="sidebar">
          <div className="sidebar-brand">
            <span>📦</span>
            <span>Склад</span>
          </div>
          <nav className="sidebar-nav">
            <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="icon">📋</span>
              <span>Товары</span>
            </NavLink>
            <NavLink to="/add" className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="icon">➕</span>
              <span>Добавить товар</span>
            </NavLink>
            <NavLink to="/upload-photo" className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="icon">📸</span>
              <span>Загрузить фото</span>
            </NavLink>
            <NavLink to="/notifications" className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="icon">🔔</span>
              <span>Уведомления</span>
            </NavLink>
          </nav>
        </aside>

        {/* Основной контент */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ProductList />} />
            <Route path="/add" element={<ProductForm />} />
            <Route path="/edit/:id" element={<ProductForm />} />
            <Route path="/upload-photo" element={<PhotoUpload />} />
            <Route path="/notifications" element={<Notifications />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

//знаки будут заменены на Font Awesome или Material Icons