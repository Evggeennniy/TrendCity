const signinBtn = document.getElementById("autoriz-btn-login");
const overlay = document.getElementById("overlay");
const authPopUp = document.getElementById("autrztn-popup");
const closePopUpBtn = document.getElementById("close-popup-btn");
const authPopupRegBtn = document.getElementById("popup-reg-btn");
const authPopupLoginBtn = document.getElementById("popup-login-btn");
const navMenuBtn = document.getElementById("nav-mob-btn");
const sliderNavMenu = document.getElementById("slider-nav-menu");
const sliderAuthBtn = document.getElementById("slider-auth-btn");
const closeSliderNavBtn = document.getElementById("close-slider-btn");
const favoriteCounter = document.getElementById("favorite-counter");

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

signinBtn != null ? signinBtn.addEventListener("click", pupupToggle) : "";
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

function addToFavoriteList(product) {
  const productId = product.getAttribute("product-id");

  let favorites = JSON.parse(localStorage.getItem("favorites")) || [];

  const index = favorites.findIndex((item) => item.id === productId);

  if (index > -1) {
    favorites.splice(index, 1);
  } else {
    const productData = {
      id: productId,
      name: product
        .querySelector(".products-list__item-title")
        .textContent.trim(),
      price: product
        .querySelector(".products-list__item-curr-price")
        .textContent.trim(),
      image: product
        .querySelector(".products-list__item-img")
        .getAttribute("src"),
    };

    favorites.push(productData);
  }

  localStorage.setItem("favorites", JSON.stringify(favorites));

  updateFavoritesUI();
}

function updateFavoritesUI() {
  let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
  favoriteCounter.textContent = favorites.length;

  const navFavoritesList = document.querySelector(".favorite-nav__list");
  if (navFavoritesList) {
    navFavoritesList.innerHTML = "";

    favorites.forEach((item) => {
      const li = document.createElement("li");
      li.classList.add("favorite-nav__item");

      li.innerHTML = `
        <img src="${item.image}" alt="img" class="favorite-nav__item-img" />
        <div class="favorite-nav__item-content">
          <div class="favorite-nav__item-stars">
            <img src="/static/star-orange-icon.svg" alt="star-icon" class="favorite-nav__item-star" />
            <!-- Повторите звездочки по необходимости -->
          </div>
          <p>${item.name}</p>
          <h5>${item.price}</h5>
        </div>
      `;

      navFavoritesList.appendChild(li);
    });
  }

  const extendedInfoList = document.querySelector(".favorite-list");
  if (extendedInfoList) {
    extendedInfoList.innerHTML = "";

    favorites.forEach((item) => {
      const li = document.createElement("li");
      li.classList.add("products-list__item");
      li.setAttribute("product-id", item.id);

      li.innerHTML = `
        <div class="product-list__img-wrap">
          <img src="${item.image}" alt="product-img" class="products-list__item-img" />
          <img src="/static/heart-orange-icon.svg" alt="" class="heart-orange-icon active" />
        </div>
        <h5 class="products-list__item-title">${item.name}</h5>
        <div class="products-list__item-info">
          <div class="products-list__item-discount">
            <div>
              <span class="products-list__item-price">${item.price}</span>
            </div>
            <h4 class="products-list__item-curr-price">${item.price}<span class="money-symbol">₴</span></h4>
          </div>
          <button class="products-list__item-button">
            <img src="/static/basket-icon.svg" alt="item-buy-icon" class="products-list__item-buy-icon" />
          </button>
        </div>
      `;

      extendedInfoList.appendChild(li);
    });
  }

  const favoriteProductIds = favorites.map((item) => item.id);

  const products = document.querySelectorAll(".products-list__item");

  products.forEach((product) => {
    const productId = product.getAttribute("product-id");
    const heartIcon = product.querySelector(".heart-orange-icon");

    if (favoriteProductIds.includes(productId)) {
      heartIcon.classList.add("active");
    } else {
      heartIcon.classList.remove("active");
    }
  });
}

updateFavoritesUI();

document.addEventListener("click", function (event) {
  if (event.target.classList.contains("heart-orange-icon")) {
    const target = event.target;
    target.classList.toggle("active");

    const product = target.closest(".products-list__item");
    addToFavoriteList(product);
  }
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
