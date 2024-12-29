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
if (sliderAuthBtn) {
  sliderAuthBtn.addEventListener("click", () => {
    sliderNavToggle();
    pupupToggle();
  });
}

document.body.addEventListener("click", (event) => {
  const target = event.target;
  if (!target.classList.contains("quantity-btn")) return;

  const quantityNav = target.closest(".quantity_item");
  if (!quantityNav) return;

  const valueOutput = quantityNav.querySelector(".quantity-value");
  let currentValue = parseInt(valueOutput.getAttribute("value")) || 1;
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

const favoriteBtn = document.getElementById("favorite-btn");
const favoriteNav = document.getElementById("favorite-nav");
const favoriteNavList = document.getElementById("favorite-nav-list");
const favoriteCounter = document.getElementById("favorite-counter");

favoriteBtn.addEventListener("click", (event) => {
  const wrapper = event.target.closest("#favorite-btn");
  const btn = wrapper.querySelector(".favorite-btn");
  btn.classList.toggle("active");
  favoriteNav.classList.toggle("active");
});

favoriteNavList.addEventListener("click", (event) => {
  event.stopPropagation();
});

function updateFavoriteUI() {
  let localData = localStorage.getItem("favorite");
  let localBasket = localStorage.getItem("basket");
  let lastIndex = localStorage.getItem("last_index");

  if (localData == null) {
    localStorage.setItem("favorite", "[]");
    return;
  }

  if (localBasket == null) {
    localStorage.setItem("basket", "[]");
    return;
  }

  if (lastIndex == null) {
    localStorage.setItem("last_index", "0");
    return;
  }

  const includedIds = new Array();

  favoriteNavList.innerHTML = "";
  for (let item of JSON.parse(localData)) {
    includedIds.push(item.productId);

    const newItem = document.createElement("div");
    newItem.classList.add("favorite-nav__item");
    newItem.innerHTML = `
      <img
        src="${item.productImg}"
        alt="img"
        class="favorite-nav__item-img"
      />
      <div class="favorite-nav__item-content">
        <p>${item.productName}</p>
      </div>
    `;
    favoriteNavList.append(newItem);
  }

  const favoriteList = document.getElementById("favorite-list");
  if (favoriteList) {
    favoriteList.innerHTML = "";
    for (let item of JSON.parse(localData)) {
      const newItem = document.createElement("li");
      newItem.classList.add("products-list__item");
      newItem.innerHTML = item.productObj;
      favoriteList.append(newItem);
    }
  }

  includedIds.forEach((id) => {
    const includedProducts = document.querySelectorAll(`.favorite-${id}`);
    includedProducts.forEach((item) => {
      item.classList.add("added");
    });
  });

  favoriteCounter.textContent = includedIds.length;
}

updateFavoriteUI();

document.addEventListener("click", (event) => {
  const target = event.target;
  if (!target.classList.contains("heart-orange-icon")) return;

  const includedInFavorite = target.classList.contains("added");
  const productId = target.getAttribute("data-product-id");
  const productObj = target.closest(".products-list__item");

  const localData = JSON.parse(localStorage.getItem("favorite"));

  if (includedInFavorite) {
    const filteredList = localData.filter(
      (item) => item.productId !== productId
    );
    localStorage.setItem("favorite", JSON.stringify(filteredList));
  } else {
    const productData = {
      productId: productId,
      productImg: productObj
        .querySelector(".products-list__item-img")
        .getAttribute("src"),
      productName: productObj.querySelector(".products-list__item-title")
        .textContent,
      productObj: productObj.innerHTML,
    };

    localData.push(productData);
    localStorage.setItem("favorite", JSON.stringify(localData));
  }

  target.classList.toggle("added");
  updateFavoriteUI();
});

const basketCounter = document.getElementById("basket-counter");
function updateBasketUi() {
  const localBasket = JSON.parse(localStorage.getItem("basket"));
  basketCounter.textContent = localBasket.length;
}

updateBasketUi();

(function () {
  const now = Date.now();
  const threeDays = 3 * 24 * 60 * 60 * 1000;
  const lastClear = parseInt(localStorage.getItem("lastClearTime"), 10);

  if (!lastClear) {
    localStorage.setItem("lastClearTime", now);
  } else if (now - lastClear > threeDays) {
    localStorage.clear();
    localStorage.setItem("lastClearTime", now);
  }
})();


document.getElementById("langSwitch").addEventListener("click", function () {
  const currentUrl = window.location.pathname; // Отримує поточний URL без домену
  const currentLang = currentUrl.startsWith("/ru/"); // Перевіряємо, чи є "ru" в URL

  if (currentLang) {
    const newUrl = currentUrl.replace("/ru/", "/");
    window.location.href = newUrl;
  } else {
    const newUrl = "/ru" + currentUrl;
    window.location.href = newUrl;
  }
});