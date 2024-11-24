const promoInput = document.getElementById("promo-input");
const promoBtn = document.getElementById("promo-btn");
const statisticList = document.getElementById("statistic-list-wrap");
const promocodeBlock = document.querySelector(".statistic__promocode");
const discountList = document.getElementById("discount-list");
const csrftoken = getCookie("csrftoken");
let promoCode;
let promoPercent;

let fullCurrentPrice;


promoBtn.addEventListener("click", () => {
  if (promoInput.value === "") {
    alert("Будь ласка, введіть промокод");
    return;
  }

  const encodedPromo = encodeURIComponent(promoInput.value);
  fetch(`/check-promocode/${encodedPromo}/`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Невірний запит");
      }
      return response.json();
    })
    .then((data) => {
      if (data.status === "success") {
        alert(`Промокод прийнято! Знижка: ${data.discount}%`);
        const newEl = document.createElement("div");
        newEl.classList.add("statistic__item");
        newEl.innerHTML = `
          <h4>Промокод ${promoInput.value}</h4>
          <h4>-${data.discount}%</h4>
        `;
        statisticList.append(newEl);
        promocodeBlock.remove();

        promoCode = promoInput.value;
        promoPercent = data.discount;
        updateStatisticsUI();
      } else {
        alert("Промокод не дійсний.");
      }
    })
    .catch((error) => {
      alert("Виникла помилка. Спробуйте ще раз.");
    });
});

function toggleItem(event) {
  event.target.classList.toggle("active");
}

function localBasketEdit(action, itemId) {
  const localBasket = JSON.parse(localStorage.getItem("basket"));

  const item = localBasket.find((item) => item.itemId == itemId);
  if (!item) return;

  switch (action) {
    case "plus":
      item.productQuantity++;
      break;
    case "minus":
      if (item.productQuantity > 1) {
        item.productQuantity--;
      }
      break;
  }

  localStorage.setItem("basket", JSON.stringify(localBasket));
  updateStatisticsUI();
}

const basketList = document.getElementById("basket-list");
function updateBasketList() {
  const localBasket = JSON.parse(localStorage.getItem("basket"));
  for (let item of localBasket) {
    const newItem = document.createElement("div");
    newItem.classList.add("basket__item", "gray-border");
    newItem.setAttribute("itemId", `${item.itemId}`);
    newItem.innerHTML = `
            <div class="basket__item-general">
                <img
                    src="/static/checkmark-icon.svg"
                    alt="checkmark"
                    class="basket__item-checkmark"
                />
                <img
                src="${item.productImg}"
                alt="product-item"
                class="basket__item-img"
                />
                <div class="basket__item-info">
                <p class="basket__item-name">${item.productName} (${item.volume
      }) - ${item.optionName}</p>
                <p class="basket__item-wraptype">${item.wrapperName != null
        ? `${item.wrapperName} / ${item.wrapperPrice}₴`
        : "Без пакування"
      }</p>
                <div class="basket__item-quantity quantity_item quantity-panel-cover-mob">
                    <div>
                    <img
                        src="/static/plus-icon.svg"
                        alt="plus"
                        action="plus"
                        class="plus basket__item-icon quantity-btn"
                        onclick="localBasketEdit('plus', ${item.itemId})"
                    />
                    <h3 class="quantity-value" value="${item.productQuantity}">
                    ${item.productQuantity}
                    </h3>
                    <img
                        src="/static/minus-icon.svg"
                        alt="minus"
                        action="minus"
                        class="minus basket__item-icon quantity-btn"
                        onclick="localBasketEdit('minus', ${item.itemId})"
                    />
                    </div>
                </div>
                </div>
            </div>
            <div class="gray-line"></div>
            <div class="basket__item-price">
                <div class="basket__item-quantity quantity_item quantity-panel-cover-pc quantity-panel-cover-pc">
                <div>
                    <img
                    src="/static/plus-icon.svg"
                    alt="plus"
                    action="plus"
                    class="plus basket__item-icon quantity-btn"
                    onclick="localBasketEdit('plus', ${item.itemId})"
                    />
                    <h3 class="quantity-value" value="${item.productQuantity}">
                    ${item.productQuantity}
                    </h3>
                    <img
                    src="/static/minus-icon.svg"
                    alt="minus"
                    action="minus"
                    class="minus basket__item-icon quantity-btn"
                    onclick="localBasketEdit('minus', ${item.itemId})"
                    />
                </div>
                </div>
                <div class="price-wrap">
                <div class="basket__item-discount" ${item.volumeDiscount == 0 ? 'style="display: none"' : ""
      }>
                    <span class="full-price">${item.volumePrice}₴</span>
                    <span class="discount-percent">-${item.volumeDiscount
      }%</span>
                </div>
                <h3>
                    ${item.currentPrice}<span class="curr-symbol">₴</span>
                </h3>
                </div>
            </div>
        `;
    basketList.append(newItem);
  }
}

updateBasketList();

basketList.addEventListener("click", (event) => {
  const target = event.target;
  if (!target.classList.contains("basket__item-checkmark")) return;

  const item = target.closest(".basket__item");
  item.classList.toggle("chosen");
});

const deleteBtn = document.getElementById("btn-delete-checked");
deleteBtn.addEventListener("click", () => {
  const checkedItems = document.querySelectorAll(".basket__item.chosen");
  let localBasket = JSON.parse(localStorage.getItem("basket"));

  checkedItems.forEach((item) => {
    const itemId = item.getAttribute("itemid");

    localBasket = localBasket.filter(
      (basketItem) => basketItem.itemId != itemId
    );

    item.remove();
  });

  localStorage.setItem("basket", JSON.stringify(localBasket));
  updateStatisticsUI();
});

const priceWithoutDiscountHeader = document.getElementById(
  "price-without-discount"
);
const priceWithDiscountHeader = document.getElementById("price-with-discount");
const wrappersPricetHeader = document.getElementById("wrappers-price");
const currentFullPriceHeader = document.getElementById("current-full-price");
function updateStatisticsUI() {
  const localBasket = JSON.parse(localStorage.getItem("basket"));
  if (localBasket.lenght) return;
  const fullPrice = localBasket.reduce(
    (sum, item) =>
      sum + parseInt(item.volumePrice) * parseInt(item.productQuantity),
    0
  );
  const discountedPrice = localBasket.reduce(
    (sum, item) =>
      sum + parseInt(item.currentPrice) * parseInt(item.productQuantity),
    0
  );
  const wrappersPrice = localBasket.reduce((sum, item) => {
    return item.wrapperPrice != null ? sum + parseInt(item.wrapperPrice) : sum;
  }, 0);

  const discountValue = fullPrice - discountedPrice;
  let currentFullPrice = discountedPrice + wrappersPrice;
  if (promoCode != undefined) {
    currentFullPrice =
      currentFullPrice - (currentFullPrice / 100) * promoPercent;
  }
  fullCurrentPrice = currentFullPrice;
  discount()
  priceWithoutDiscountHeader.textContent = `${fullPrice}₴`;
  priceWithDiscountHeader.textContent = `-${discountValue}₴`;
  wrappersPricetHeader.textContent = `${wrappersPrice}₴`;
  currentFullPriceHeader.textContent = `${currentFullPrice}₴`;
}

updateStatisticsUI();

function discount() {
  const localBasket = JSON.parse(localStorage.getItem("basket"));
  const categorySummary = localBasket.reduce((acc, item) => {
    const categoryId = item.categoryId || "null";
    const currentPrice = parseFloat(item.currentPrice);
    const quantity = parseInt(item.productQuantity, 10);
    if (!acc[categoryId]) {
      acc[categoryId] = {
        totalAmount: 0,
        totalQuantity: 0
      };
    }

    acc[categoryId].totalAmount += currentPrice * quantity;
    acc[categoryId].totalQuantity += quantity;
    acc.totalAmount = (acc.totalAmount || 0) + currentPrice * quantity;
    acc.totalQuantity = (acc.totalQuantity || 0) + quantity;

    return acc;
  }, {});
  fetch("/discount/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(categorySummary),
  })
    .then(response => response.json())
    .then(data => {
      console.log("Результат запиту:", data);
      localStorage.setItem("activeDiscount", data.freeDelivery.join("\n"));
      discountList.innerHTML = "";
      data.freeDelivery.forEach(promo => {
        addItemDiscount(promo);
      });
    })
    .catch(error => {
      console.error("Помилка запиту:", error);
    });

}

function addItemDiscount(promo) {
  const promoItem = document.createElement("p");
  promoItem.classList.add("promo-item");
  promoItem.style.margin = "10px 0";
  promoItem.textContent = promo;
  discountList.appendChild(promoItem);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const form = document.querySelector(".order-form__form");
form.addEventListener("submit", function (event) {
  event.preventDefault();

  const localBasket = JSON.parse(localStorage.getItem("basket"));
  const activeDiscount = localStorage.getItem("activeDiscount");
  const data = {
    name: document.getElementById("order-form__name").value,
    surname: document.getElementById("order-form__surname").value,
    country_code: document.getElementById("order-form__phone-code").value,
    number: document.getElementById("order-form__phone-num").value,
    payment_method: document.getElementById("order-form__paymethod").value,
    delivery_type: document.getElementById("order-form__deltype").value,
    post_office_id: document.getElementById("order-form__novaid").value,
    comment: document.getElementById("order-form__text").value,
    order_list: localBasket,
    active_discount: activeDiscount,
    full_price: fullCurrentPrice,
    promocode: {
      id: promoCode,
      percent: promoPercent,
    },
  };


  // Send data to the server using Fetch API
  fetch("/submit-order/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.ok) {
        localStorage.removeItem("basket");
        window.location.reload();
        alert("Замовлення створено!");
      } else {
        alert("Помилка замовлення!");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
