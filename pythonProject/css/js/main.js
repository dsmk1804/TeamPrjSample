const categoryBtn = document.getElementById('categoryBtn');
const dropdownMenu = document.getElementById('dropdownMenu');

function showDropdownMenu() {
  dropdownMenu.style.display = 'block';
}

function hideDropdownMenu() {
  dropdownMenu.style.display = 'none';
}

function keepDropdownMenu() {
  dropdownMenu.style.display = 'block';
}

categoryBtn.addEventListener('mouseenter', showDropdownMenu);
categoryBtn.addEventListener('mouseleave', hideDropdownMenu);

dropdownMenu.addEventListener('mouseenter', keepDropdownMenu);
dropdownMenu.addEventListener('mouseleave', hideDropdownMenu);


// 마켓컬리 버전입니다.
// 출처: https://github.com/fhypothesis/Publishing-work/blob/main/kurly/js/main.js