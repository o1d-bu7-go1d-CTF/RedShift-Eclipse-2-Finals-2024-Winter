const inputField = document.getElementById('inputField');
const clearButton = document.getElementById('clearButton');

// Обработчик для кнопок с буквами
document.querySelectorAll('.keebs-container span').forEach(button => {
    button.addEventListener('click', function () {
        const letter = this.textContent;
        inputField.value += letter;
    });
});

// Обработчик для кнопки очистки input
clearButton.addEventListener('click', function () {
    inputField.value = '';  // Очищаем поле ввода
});