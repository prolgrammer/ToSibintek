Для запуска приложения введите:
  npm i
  dev режим
    npm run dev
  docker
    docker build -t frontend .
    docker run -d -p 3000:3000 frontend
  prod режим без docker
    npm run preview
