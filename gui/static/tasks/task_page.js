let descriptionDiv = document.getElementById('task-description');
descriptionDiv.style.fontSize = '16px';
const plusIcon = document.querySelector('.plus-icon');
const minusIcon = document.querySelector('.minus-icon');
plusIcon.addEventListener('click', () => {
    setFontSize('+');
});
minusIcon.addEventListener('click', () => {
    setFontSize('-');
});


function setFontSize(operation) {
    descriptionDiv = document.getElementById('task-description');
    let currSize = +descriptionDiv.style.fontSize.match(/^[\d.]+/);
    currSize = eval(`${currSize}${operation}7`);
    descriptionDiv.style.fontSize = `${currSize}px`
}
