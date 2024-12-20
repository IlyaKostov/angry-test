document.addEventListener('DOMContentLoaded', function () {
    const interval = 2000; // Интервал проверки в миллисекундах (2 секунда)
    let checkAuthInterval = null;

    function checkAuthorization() {
        fetch("{% url 'users:check_auth' %}")
            .then(response => response.json())
            .then(data => {
                if (data.authenticated) {
                    // Если пользователь авторизован, обновить страницу
                    window.location.reload();
                }
            })
            .catch(error => console.error('Ошибка проверки авторизации:', error));
    }

    const telegramLoginBtn = document.getElementById('telegram-login-btn');
    const modal = document.getElementById('telegramModal');

    // Запуск проверки при клике на кнопку "Войти через Telegram"
    telegramLoginBtn.addEventListener('click', function () {
        if (!checkAuthInterval) {
            checkAuthInterval = setInterval(checkAuthorization, interval);
        }
    });

    // Остановить проверку при закрытии модального окна
    modal.addEventListener('hidden.bs.modal', function () {
        if (checkAuthInterval) {
            clearInterval(checkAuthInterval);
            checkAuthInterval = null; // Сбрасываем интервал
        }
    });
});