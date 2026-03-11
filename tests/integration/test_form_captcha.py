# Маркер: integration, regression
# Тест 1: Валидный токен (имитация Google reCaptcha)
# Отправляем POST на свой сайт с правильным токеном reCaptcha
# Ожидаем: 200 OK, письмо ушло

# Тест 2: Пустой токен
# Ожидаем: 400 Bad Request, "reCaptcha required"

# Тест 3: Невалидный токен (поддельный)
# Ожидаем: 403 Forbidden, "Invalid reCaptcha"

# Тест 4: Таймаут (если Google не отвечает)
# Мокаем недоступность Google, проверяем что сайт падает (ошибка 503)