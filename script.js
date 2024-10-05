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

// PRODUCT
const photosList = document.querySelector(".photos__imgs-list");

photosList.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.classList.contains("photos__imgs-item")) return;

  const prevImg = document.querySelector(".photos__imgs-item.active");
  const prevCircle = document.querySelector(".circle.active");

  const newImgId = target.getAttribute("image-id");

  const newCircle = document.querySelector(`#circle-${newImgId}`);

  if (prevImg) {
    prevImg.classList.remove("active");
  }

  if (prevCircle) {
    prevCircle.classList.remove("active");
  }

  target.classList.add("active");
  newCircle.classList.add("active");
});

const scrollContainer = document.querySelector(".scroll-container");
const circles = document.querySelectorAll(".photos__general-nav .circle");
const images = document.querySelectorAll(".photos__general-img");

scrollContainer.addEventListener("scroll", () => {
  const scrollPosition = scrollContainer.scrollLeft;
  const containerWidth = scrollContainer.clientWidth;

  // Вычисляем активный индекс
  let activeIndex = Math.round(scrollPosition / containerWidth);

  // Ограничиваем активный индекс
  if (activeIndex < 0) activeIndex = 0;
  if (activeIndex >= images.length) activeIndex = images.length - 1;

  // Обновляем классы кружочков
  circles.forEach((circle, index) => {
    circle.classList.toggle("active", index === activeIndex);
  });
});

let chosenProductVolume = document.querySelector(".volume-item.chosen");
const productVolumeslist = document.getElementById("product-volumes-list");
productVolumeslist.addEventListener("click", (event) => {
  const target = event.target;
  if (!target.classList.contains("volume-item")) return;

  chosenProductVolume.classList.toggle("chosen");
  chosenProductVolume = target;
  target.classList.toggle("chosen");
});

const likeBtn = document.getElementById("like-btn");
likeBtn.addEventListener("click", (event) => {
  event.target.closest(".nav__like-btn").classList.toggle("active");
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

const addProductBtns = document.querySelectorAll(".add-switch-btn");
addProductBtns.forEach((item) => {
  item.addEventListener("click", (event) => {
    const btn = event.target.closest(".add-switch-btn");
    btn.classList.toggle("success");
  });
});

let chosenProductType = document.querySelector(".variations__item.chosen");
const productTypes = document.querySelectorAll(".variations__item");

productTypes.forEach((item) => {
  item.addEventListener("click", (event) => {
    const target = event.target.closest(".variations__item");
    if (chosenProductType) {
      chosenProductType.classList.remove("chosen");
    }
    target.classList.add("chosen");
    chosenProductType = target;
  });
});

let chosenProductWrapper = document.querySelector(".wrapper__item.chosen");
const productWrappersList = document.getElementById("product-wrapper-list");
productWrappersList.addEventListener("click", (event) => {
  const target = event.target.closest(".wrapper__item");
  if (!target || target === chosenProductWrapper) return;
  if (chosenProductWrapper) {
    chosenProductWrapper.classList.remove("chosen");
  }
  target.classList.add("chosen");
  chosenProductWrapper = target;
});

const componentList = document.getElementById("components-list");
componentList.addEventListener("click", (event) => {
  const target = event.target;
});

const imageContainer = document.querySelector(".image-container");
const image = document.querySelector(".image");
const lens = document.querySelector(".zoom-lens");

imageContainer.addEventListener("mousemove", zoom);

imageContainer.addEventListener("mouseenter", () => {
  lens.style.display = "block";
});

imageContainer.addEventListener("mouseleave", () => {
  lens.style.display = "none";
});

function zoom(e) {
  const rect = imageContainer.getBoundingClientRect();

  const x = e.pageX - rect.left;
  const y = e.pageY - rect.top;

  const lensX = e.pageX;
  const lensY = e.pageY - 50;

  lens.style.left = lensX + "px";
  lens.style.top = lensY + "px";

  if (
    x > 0 &&
    x < rect.width &&
    y > 0 &&
    y < rect.height &&
    window.innerWidth >= 576
  ) {
    lens.style.display = "block"; // Показываем элемент lens
  } else {
    lens.style.display = "none"; // Скрываем элемент lens
  }

  const backgroundX = (x / rect.width) * 100;
  const backgroundY = (y / rect.height) * 100;

  lens.style.backgroundPosition = `${backgroundX}% ${backgroundY}%`;
}

imageContainer.addEventListener("mousemove", zoom);

const moreReviewsBtn = document.getElementById("more-reviews-btn");
const reviewsList = document.getElementById("reviews-list");
moreReviewsBtn.addEventListener("click", () => {
  const newReviews = `
    <li class="reviews__item">
      <div class="reviews__item-content">
        <p class="reviews__item-username">Дмитро Сиренченко</p>
        <div class="reviews__item-grade">
          <div class="reviews__item-line"></div>
          <div class="reviews__item-value">
            <img
              src="./star-icon.svg"
              alt="star-icon"
              class="reviews__item-icon"
            />
            <span>4,8</span>
          </div>
        </div>
      </div>
      <p class="reviews__item-text">
        Стильно виглядає, танаповнює машину приємним,
        ненав’язливим ароматом☺️
      </p>
    </li>
    <li class="reviews__item">
      <div class="reviews__item-content">
        <p class="reviews__item-username">Дмитро Сиренченко</p>
        <div class="reviews__item-grade">
          <div class="reviews__item-line"></div>
          <div class="reviews__item-value">
            <img
              src="./star-icon.svg"
              alt="star-icon"
              class="reviews__item-icon"
            />
            <span>4,8</span>
          </div>
        </div>
      </div>
      <p class="reviews__item-text">
        Стильно виглядає, танаповнює машину приємним,
        ненав’язливим ароматом☺️
      </p>
    </li>`;
  reviewsList.insertAdjacentHTML("beforeend", newReviews);
});

const createReviewPopup = document.getElementById("create-review-popup");
const createReviewBtn = document.getElementById("create-review-btn");
const closeReviewPopup = document.getElementById("close-review-popup");

const toggleReviewPopup = () => {
  overlay.classList.toggle("active");
  createReviewPopup.classList.toggle("active");
};

createReviewBtn.addEventListener("click", toggleReviewPopup);
closeReviewPopup.addEventListener("click", toggleReviewPopup);

const stars = document.querySelectorAll(".star-icon");

stars.forEach((star, index) => {
  star.addEventListener("click", () => {
    const rating = index + 1;

    stars.forEach((s, i) => {
      if (i < rating) {
        s.classList.add("yellow");
      } else {
        s.classList.remove("yellow");
      }
    });
  });
});
