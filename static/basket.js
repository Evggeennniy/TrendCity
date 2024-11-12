{
  /* <div class="basket__item chosen gray-border">
  
</div>; */
}

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
                <p class="basket__item-name">${item.productName} (${
      item.volume
    }) - ${item.optionName}</p>
                <p class="basket__item-wraptype">${
                  item.wrapperName != null
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
                <div class="basket__item-discount" ${
                  item.volumeDiscount == 0 ? 'style="display: none"' : ""
                }>
                    <span class="full-price">${item.volumePrice}₴</span>
                    <span class="discount-percent">-${
                      item.volumeDiscount
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
  const currentFullPrice = discountedPrice + wrappersPrice;

  priceWithoutDiscountHeader.textContent = `${fullPrice}₴`;
  priceWithDiscountHeader.textContent = `-${discountValue}₴`;
  wrappersPricetHeader.textContent = `${wrappersPrice}₴`;
  currentFullPriceHeader.textContent = `${currentFullPrice}₴`;
}

updateStatisticsUI();

const form = document.querySelector(".order-form__form");
form.addEventListener("submit", function (event) {
  event.preventDefault();

  const localBasket = JSON.parse(localStorage.getItem("basket"));

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
  };

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
  const csrftoken = getCookie("csrftoken");

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
