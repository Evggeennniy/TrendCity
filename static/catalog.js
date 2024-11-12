const filterNavBtn = document.getElementById("slider-filter-btn");
const closeFilterNavBtn = document.getElementById("close-slider-filter-btn");
const mainPanel = document.getElementById("main-panel");

const sliderFilterToggle = () => {
  overlay.classList.toggle("active");
  mainPanel.classList.toggle("active");
};

filterNavBtn.addEventListener("click", sliderFilterToggle);
closeFilterNavBtn.addEventListener("click", sliderFilterToggle);

const minRange = document.getElementById("minRange");
const maxRange = document.getElementById("maxRange");
const minValue = document.getElementById("minValue");
const maxValue = document.getElementById("maxValue");

minRange.addEventListener("input", () => {
  if (parseInt(minRange.value) > parseInt(maxRange.value)) {
    minRange.value = maxRange.value;
  }
  minValue.value = minRange.value;
  updateSliderFill();
});

maxRange.addEventListener("input", () => {
  if (parseInt(maxRange.value) < parseInt(minRange.value)) {
    maxRange.value = minRange.value;
  }
  maxValue.value = maxRange.value;
  updateSliderFill();
});

function updateSliderFill() {
  const rangeSlider = document.querySelector(".range-slider");
  const percentMin = (minRange.value / minRange.max) * 100;
  const percentMax = (maxRange.value / maxRange.max) * 100;

  rangeSlider.style.background = `linear-gradient(to right, #ddd ${
    percentMin == 0 ? 5 : percentMin
  }%, #FF6600 ${percentMin}%, #FF6600 ${percentMax}%, #ddd ${percentMax}%)`;
}

updateSliderFill();

// IN A CASE FOR MANUAL SETTINGS !! TO DO
// minValue.addEventListener("input", updateSliserValues);
// maxValue.addEventListener("input", updateSliserValues);

// function updateSliserValues() {
//   const absolutMin = minRange.getAttribute("min");
//   const absolutMax = maxRange.getAttribute("max");

//   const newMinValue = minValue.value;
//   const newMaxValue = maxValue.value;

//   minRange.setAttribute("value", newMinValue);
//   maxRange.setAttribute("value", newMaxValue);
//   updateSliderFill();
// }

// Функция для сбора всех выбранных фильтров и формирования URL
function updateFilters() {
  const params = new URLSearchParams(window.location.search);

  // Обрабатываем все чекбоксы
  document
    .querySelectorAll('input[type="checkbox"]')
    .forEach(function (checkbox) {
      if (checkbox.checked) {
        if (checkbox.name === "brand" || checkbox.name === "gender") {
          // Удаляем все значения и добавляем выбранные
          params.delete(checkbox.name);
          document
            .querySelectorAll('input[name="' + checkbox.name + '"]:checked')
            .forEach(function (checkedBox) {
              params.append(checkbox.name, checkedBox.value);
            });
        } else {
          params.set(checkbox.name, checkbox.value);
        }
      } else {
        if (checkbox.name === "brand" || checkbox.name === "gender") {
          // Удаляем конкретное значение
          const values = params.getAll(checkbox.name);
          params.delete(checkbox.name);
          values.forEach(function (value) {
            if (value !== checkbox.value) {
              params.append(checkbox.name, value);
            }
          });
        } else {
          params.delete(checkbox.name);
        }
      }
    });

  // Обрабатываем диапазон цен
  const minPrice = document.getElementById("minValue").value;
  const maxPrice = document.getElementById("maxValue").value;
  params.set("min_price", minPrice);
  params.set("max_price", maxPrice);

  // Формируем новый URL
  const newUrl = `${window.location.pathname}?${params.toString()}`;

  // Перенаправляем на новый URL
  window.location.href = newUrl;
}

// Добавляем обработчики событий на чекбоксы
document
  .querySelectorAll('input[type="checkbox"]')
  .forEach(function (checkbox) {
    checkbox.addEventListener("change", updateFilters);
  });

// Обработчики событий для диапазона цен
document.getElementById("minRange").addEventListener("input", function () {
  document.getElementById("minValue").value = this.value;
});
document.getElementById("maxRange").addEventListener("input", function () {
  document.getElementById("maxValue").value = this.value;
});
document.getElementById("minRange").addEventListener("change", updateFilters);
document.getElementById("maxRange").addEventListener("change", updateFilters);

const sortButton = document.getElementById("sortButton");
const sortDropdown = document.getElementById("sortDropdown");

// Функция для переключения видимости выпадающего меню
sortButton.addEventListener("click", function (event) {
  event.preventDefault();
  sortDropdown.style.display =
    sortDropdown.style.display === "none" ? "block" : "none";
});

// Закрываем меню при клике вне его
document.addEventListener("click", function (event) {
  if (
    !sortButton.contains(event.target) &&
    !sortDropdown.contains(event.target)
  ) {
    sortDropdown.style.display = "none";
  }
});

// Обработка выбора опции сортировки
document.querySelectorAll(".sort-option").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.preventDefault();
    const sortValue = this.getAttribute("data-sort");
    updateSorting(sortValue);
  });
});

// Функция для обновления параметра сортировки
function updateSorting(sortValue) {
  const params = new URLSearchParams(window.location.search);

  // Устанавливаем новый параметр 'sort'
  params.set("sort", sortValue);

  // Формируем новый URL
  const newUrl = `${window.location.pathname}?${params.toString()}`;

  // Перенаправляем на новый URL
  window.location.href = newUrl;
}
