document.addEventListener('DOMContentLoaded', function() {
    // Найти все всплывающие окна
    const popups = document.querySelectorAll('.popup-message');

    // Добавить обработчик событий для каждой кнопки закрыть
    popups.forEach(function(popup) {
        const closeButton = popup.querySelector('.close');
        closeButton.addEventListener('click', function() {
            popup.style.display = 'none'; // Скрыть всплывающее окно
        });
    });

    // Также можно добавить автоматическое скрытие через время
    setTimeout(function() {
        popups.forEach(function(popup) {
            popup.style.display = 'none';
        });
    }, 5000); // Скрыть сообщения через 5 секунд
});