const signinBtn = document.getElementById("autoriz-btn");
const overlay = document.getElementById("overlay");
const authPopUp = document.getElementById("autrztn-popup");
const closePopUpBtn = document.getElementById("close-popup-btn");
const authPopupRegBtn = document.getElementById("popup-reg-btn");
const authPopupLoginBtn = document.getElementById("popup-login-btn");
const navMenuBtn = document.getElementById("nav-mob-btn");
const sliderNavMenu = document.getElementById("slider-nav-menu");
const sliderAuthBtn = document.getElementById("slider-auth-btn");
const closeSliderNavBtn = document.getElementById("close-slider-btn");

const pupupToggle = () => {
  overlay.classList.toggle("active");
  authPopUp.classList.toggle("active");
};

const popupAuthContentToggle = () => {
  authPopUp.classList.toggle("registration");
};

const sliderNavToggle = () => {
  overlay.classList.toggle("active");
  sliderNavMenu.classList.toggle("active");
};

signinBtn.addEventListener("click", pupupToggle);
closePopUpBtn.addEventListener("click", pupupToggle);
authPopupRegBtn.addEventListener("click", popupAuthContentToggle);
authPopupLoginBtn.addEventListener("click", popupAuthContentToggle);
navMenuBtn.addEventListener("click", sliderNavToggle);
closeSliderNavBtn.addEventListener("click", sliderNavToggle);
sliderAuthBtn.addEventListener("click", () => {
  sliderNavToggle();
  pupupToggle();
});

const favoriteBtn = document.getElementById("favorite-btn");
const favoriteNav = document.getElementById("favorite-nav");
favoriteBtn.addEventListener("click", (event) => {
  const wrapper = event.target.closest("#favorite-btn");
  const btn = wrapper.querySelector(".favorite-btn");
  btn.classList.toggle("active");
  favoriteNav.classList.toggle("active");
});

favoriteNav.addEventListener("click", (event) => {
  event.stopPropagation();
});

const likeBtns = document.querySelectorAll(".heart-orange-icon");
likeBtns.forEach((item) => {
  item.addEventListener("click", (event) => {
    event.target.classList.toggle("active");
  });
});

const quantityNavs = document.querySelectorAll(".quantity_item");
quantityNavs.forEach((item) => {
  item.addEventListener("click", (event) => {
    const target = event.target;
    if (!target.classList.contains("quantity-btn")) return;
    const quantityNav = target.closest(".quantity_item");
    const valueOutput = quantityNav.querySelector(".quantity-value");
    let currentValue = valueOutput.getAttribute("value");
    const action = target.getAttribute("action");

    switch (action) {
      case "plus":
        currentValue++;
        break;
      case "minus":
        if (currentValue > 1) {
          currentValue--;
        }
        break;
    }

    valueOutput.setAttribute("value", currentValue);
    valueOutput.textContent = currentValue;
  });
});
