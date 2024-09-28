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

function formatPhone(input) {
  let value = input.value.replace(/\D/g, "");

  if (value.length > 9) {
    value = value.substring(0, 9);
  }

  if (value.length > 6) {
    input.value = value.replace(
      /(\d{2})(\d{2})(\d{2})(\d{0,3})/,
      "$1 $2 $3 $4"
    );
  } else if (value.length > 4) {
    input.value = value.replace(/(\d{2})(\d{2})(\d{0,2})/, "$1 $2 $3");
  } else if (value.length > 2) {
    input.value = value.replace(/(\d{2})(\d{0,2})/, "$1 $2");
  } else {
    input.value = value;
  }
}
