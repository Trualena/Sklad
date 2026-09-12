import {defineConfig} from 'vite';// создание объекта конфигурации и автодополнение  
import react from '@vitejs/plugin-react';//компиляция JSX В JS
import {VitePWA} from 'vite-plugin-pwa';//сборка пва.

export default defineConfig({
  plugins: [
    react(),//ПЛАГИН РЕАКТ 
    VitePWA({//ПОДДЕРЖКА ПВА 
      registerType: 'autoUpdate',//обноление новой версии у пользователя автоматически при обновлении на сервере 
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],//файлы в кэше
      manifest: {//отображение на тф 
        name: 'Складская система WMS',//имя в списке приложений и на экране установки
        short_name: 'WMS Склад',//на главном экране 
        description: 'Система управления складскими запасами',
        theme_color: '#2d3b52',//строка состояния 
        background_color: '#f0f2f5',//при загрузке 
        display: 'standalone',   //приложение открывается без адресной строки браузера
        orientation: 'portrait',
        scope: '/',//все URL начинающиеся с / будут обрабатываться приложением
        start_url: '/',
        icons: [{src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'},
          {src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'},
          {src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'},
          {src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'}],
      },
    }),
  ],
  //Фронтенд http://localhost:5173 порт Vite
  // Бэкенд Django http://127.0.0.1:8000.
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',//куда перенаправлять запрос 
        changeOrigin: true,//подмена адреса с запросом на адрес джанго 
        secure: false,//проверка сертификата (при разработке)
      },
      '/media': {//при загрузке медиа 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
