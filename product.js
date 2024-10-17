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

circles[0].classList.add("active");
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
});

scrollContainer.addEventListener("scroll", () => {
  const scrollPosition = scrollContainer.scrollLeft;
  const containerWidth = scrollContainer.clientWidth;

  let activeIndex = Math.round(scrollPosition / containerWidth);

  if (activeIndex < 0) activeIndex = 0;
  if (activeIndex >= images.length) activeIndex = images.length - 1;

  circles.forEach((circle, index) => {
    circle.classList.toggle("active", index === activeIndex);
  });
});

const imgContainer = document.querySelector(".image-container");
const smlImages = document.querySelectorAll(".photos__imgs-item");
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
  console.log(img);
  img.scrollIntoView({
    behavior: "smooth",
    block: "center",
    inline: "center",
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
