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
