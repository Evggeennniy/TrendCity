const reviewslink = document.getElementById("reviews-link");
const reviewslist = document.getElementById("reviews-list");
reviewslink.addEventListener("click", () => {
  reviewslist.scrollIntoView({
    behavior: "smooth",
    block: "center",
  });
});

const scrollContainer = document.querySelector(".scroll-container");
const circlesContainer = document.getElementById("circles-container");
const circles = document.querySelectorAll(".photos__general-nav .circle");
const images = document.querySelectorAll(".photos__general-img");

const zoomLens = document.querySelector("#photo-lens-zoom");
function updateZoomLens(index) {
  let currentObj = circles[index];
  if (!currentObj) return;
  currentObj = currentObj.getAttribute("objid");
  const currentImg = scrollContainer.querySelector(
    `#product-main-img-${currentObj}`
  );
  zoomLens.style.background = `url('${currentImg.getAttribute("src")}')`;
  zoomLens.style.backgroundSize = "1000%";
}

let lastActiveIndex;
scrollContainer.addEventListener("scroll", () => {
  const scrollPosition = scrollContainer.scrollLeft;
  const containerWidth = scrollContainer.clientWidth;

  let activeIndex = Math.round(scrollPosition / containerWidth);
  if (activeIndex == lastActiveIndex) return;
  lastActiveIndex = activeIndex;

  if (activeIndex < 0) activeIndex = 0;
  if (activeIndex >= images.length) activeIndex = images.length;

  circles.forEach((circle, index) => {
    circle.classList.toggle("active", index === activeIndex);
  });

  if (window.innerWidth >= 576) {
    updateZoomLens(activeIndex);
  }
});
updateZoomLens(0);

const imgContainer = document.querySelector(".image-container");
const smlImages = document.querySelectorAll(".photos__imgs-item");
if (smlImages[0] !== undefined) {
  smlImages[0].classList.add("active");
}
imgContainer.style.scrollBehavior = "smooth";
const photosList = document.querySelector(".photos__imgs-list");
photosList.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.classList.contains("photos__imgs-item")) return;

  smlImages.forEach((item) => {
    if (item.classList.contains("active")) {
      item.classList.remove("active");
    }
  });
  target.classList.add("active");

  const objectId = target.getAttribute("objid");
  const img = scrollContainer.querySelector(`#product-main-img-${objectId}`);

  img.scrollIntoView({
    behavior: "smooth",
    block: "center",
    inline: "center",
  });
});

if (circles[0] !== undefined) {
  circles[0].classList.add("active");
}

circlesContainer.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.classList.contains("circle")) return;

  const objectId = target.getAttribute("objid");
  const img = scrollContainer.querySelector(`#product-main-img-${objectId}`);
  img.scrollIntoView({
    behavior: "smooth",
    block: "center",
    inline: "center",
  });

  const smlImg = photosList.querySelector(`#sml-photo-${objectId}`);
  smlImages.forEach((item) => {
    if (item.classList.contains("active")) {
      item.classList.remove("active");
    }
  });
  smlImg.classList.add("active");
});

const variationsHeader = document.querySelector(".variations__header");
const firstOption = document.querySelector(".variations__item");
if (firstOption !== null) {
  firstOption.classList.add("chosen");
}
if (variationsHeader !== null) {
  variationsHeader.addEventListener("click", (event) => {
    const variationsBlock = event.target.closest(".product__variations");

    variationsBlock.classList.toggle("active");
  });
}

const productVolumesList = document.getElementById("product-volumes-list");
let chosenProductVolume = productVolumesList.querySelector(".volume-item");
const discountInfo = document.getElementById("discount-info");
const fullPrice = document.getElementById("full-price");
const currentPrice = document.getElementById("current-price");
const discountValue = document.getElementById("discount-value");
if (chosenProductVolume) {
  chosenProductVolume.classList.add("chosen");
}
productVolumesList.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.classList.contains("volume-item")) return;

  if (chosenProductVolume) {
    chosenProductVolume.classList.remove("chosen");
  }

  chosenProductVolume = target;
  chosenProductVolume.classList.add("chosen");
  updateOptionPrice();
});

function updateOptionPrice() {
  const price = chosenProductVolume.getAttribute("price");
  const discount = chosenProductVolume.getAttribute("discount");
  if (discount > 0) {
    discountInfo.style.display = "block";
    fullPrice.textContent = price + "₴";
    currentPrice.textContent = price - (price / 100) * discount;
    discountValue.textContent = discount;
  } else {
    discountInfo.style.display = "none";
    currentPrice.textContent = price;
  }
}
updateOptionPrice();

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

const createReviewPopup = document.getElementById("create-review-popup");
const createReviewBtn = document.getElementById("create-review-btn");
const closeReviewPopup = document.getElementById("close-review-popup");

const toggleReviewPopup = () => {
  overlay.classList.toggle("active");
  createReviewPopup.classList.toggle("active");
};

createReviewBtn.addEventListener("click", toggleReviewPopup);
closeReviewPopup.addEventListener("click", toggleReviewPopup);

const ratingInput = document.getElementById("rating-value");
const stars = document.querySelectorAll(".star-icon");
stars.forEach((star, index) => {
  star.addEventListener("click", () => {
    const rating = index + 1;

    ratingInput.value = rating;

    stars.forEach((s, i) => {
      if (i < rating) {
        s.classList.add("yellow");
      } else {
        s.classList.remove("yellow");
      }
    });
  });
});

const reviews = document.querySelectorAll(".reviews__item.hidden-review");
const loadMoreButton = document.getElementById("more-reviews-btn");

let currentIndex = 0;

loadMoreButton.addEventListener("click", function () {
  for (let i = currentIndex; i < currentIndex + 3 && i < reviews.length; i++) {
    reviews[i].style.display = "block";
    reviews[i].classList.remove("hidden-review");
  }

  currentIndex += 3;

  if (currentIndex >= reviews.length) {
    loadMoreButton.style.display = "none";
  }
});

const likeBtn = document.getElementById("like-btn");
likeBtn.addEventListener("click", () => {
  const productId = document
    .querySelector(".heart-orange-icon")
    .getAttribute("data-product-id");
  const productObj = document.querySelector(".products-list__item");
  const localData = JSON.parse(localStorage.getItem("favorite"));

  if (!likeBtn.classList.contains("active")) {
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

    likeBtn.classList.add("active");
  } else {
    const filteredList = localData.filter(
      (item) => item.productId !== productId
    );
    localStorage.setItem("favorite", JSON.stringify(filteredList));
    likeBtn.classList.remove("active");
  }

  updateFavoriteUI();
});

function updateProductUI() {
  const localData = JSON.parse(localStorage.getItem("favorite"));
  const productId = likeBtn.getAttribute("data-product-id");
  for (let item of localData) {
    if (item.productId == productId) {
      likeBtn.classList.add("active");
      break;
    }
  }
}

const addProductBtn = document.getElementById("add-product-btn");
addProductBtn.addEventListener("click", () => {
  const productId = document.getElementById("product-id");
  const productImg = document.querySelector(".product-main-img");
  const productTitle = document.getElementById("main-product-title");
  const productVolume = document.querySelector(".volume-item.chosen");
  const productOption = document.querySelector(".variations__item.chosen");
  const productWrapper = document.querySelector(".wrapper__item.chosen");
  const productPrice = document.getElementById("current-price");
  const productQuantity = document.getElementById("product-quantity");

  const localBasket = JSON.parse(localStorage.getItem("basket"));
  let localIndex = JSON.parse(localStorage.getItem("last_index"));

  const order = {
    itemId: localIndex++,
    productId: productId.textContent,
    productImg: productImg.getAttribute("src"),
    productName: productTitle.textContent.trim(),
    optionName: productOption.getAttribute("name"),
    volume: productVolume.getAttribute("volume"),
    volumeId: productVolume.getAttribute("id"),
    volumePrice: productVolume.getAttribute("price"),
    volumeDiscount: productVolume.getAttribute("discount"),
    wrapperName: productWrapper.getAttribute("name"),
    wrapperId: productWrapper.getAttribute("id"),
    wrapperPrice: productWrapper.getAttribute("price"),
    productQuantity: productQuantity.getAttribute("value"),
    currentPrice: productPrice.textContent,
  };

  localBasket.push(order);
  localStorage.setItem("basket", JSON.stringify(localBasket));
  localStorage.setItem("last_index", JSON.stringify(localIndex));

  updateBasketUi();
  updateProductUI();

  addProductBtn.disabled = true;

  addProductBtn.classList.add("success");
  setTimeout(() => {
    if (addProductBtn.classList.contains("success")) {
      addProductBtn.classList.remove("success");
      addProductBtn.disabled = false;
    }
  }, 2000);
});

updateProductUI();

const accesoriesList = document.getElementById("components-list");
accesoriesList.addEventListener("click", (event) => {
  const target = event.target;

  if (!target.classList.contains("components__item-btn")) return;

  const productEl = target.closest(".components__item");
  const localBasket = JSON.parse(localStorage.getItem("basket"));
  let localIndex = JSON.parse(localStorage.getItem("last_index"));

  const order = {
    itemId: localIndex++,
    productId: productEl.getAttribute("id"),
    productImg: productEl.getAttribute("img"),
    productName: productEl.getAttribute("name"),
    optionName: productEl.getAttribute("option"),
    volume: productEl.getAttribute("volume"),
    volumeId: productEl.getAttribute("volumeId"),
    volumePrice: productEl.getAttribute("volumePrice"),
    volumeDiscount: productEl.getAttribute("volumeDiscount"),
    wrapperName: null,
    wrapperId: null,
    wrapperPrice: null,
    productQuantity: productEl
      .querySelector(".quantity-value")
      .getAttribute("value"),
    currentPrice:
      productEl.getAttribute("volumePrice") -
      (productEl.getAttribute("volumePrice") / 100) *
        productEl.getAttribute("volumeDiscount"),
  };

  localBasket.push(order);
  localStorage.setItem("basket", JSON.stringify(localBasket));
  localStorage.setItem("last_index", JSON.stringify(localIndex));

  updateBasketUi();
  updateProductUI();

  target.disabled = true;

  target.classList.add("success");
  setTimeout(() => {
    if (addProductBtn.classList.contains("success")) {
      addProductBtn.classList.remove("success");
      addProductBtn.disabled = false;
    }
  }, 2000);
});
