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
