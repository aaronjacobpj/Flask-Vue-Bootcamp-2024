// EventHub - small JavaScript helpers. The app works without JS; this only improves the UI.
// Every check here is repeated on the server, because JavaScript can be switched off or bypassed.

document.addEventListener("DOMContentLoaded", () => {
  setupRegisterForm();
  setupBookingForm();
});

// 1. Register: warn immediately if the two passwords differ.
function setupRegisterForm() {
  const form = document.getElementById("register-form");
  if (!form) return;
  const password = form.querySelector("#password");
  const confirm = form.querySelector("#confirm");

  const check = () => {
    confirm.setCustomValidity(confirm.value === password.value ? "" : "Passwords do not match.");
  };
  password.addEventListener("input", check);
  confirm.addEventListener("input", check);
}

// 2. Booking: show the total price as seats change, and fetch the latest seat count from our API.
function setupBookingForm() {
  const form = document.getElementById("booking-form");
  if (!form) return;
  const price = Number(form.dataset.price);
  const seatsInput = form.querySelector("#seats");
  const total = document.getElementById("total-price");
  const seatsLeft = document.getElementById("seats-left");

  seatsInput.addEventListener("input", () => {
    total.textContent = (price * (Number(seatsInput.value) || 0)).toFixed(0);
  });

  // fetch() calls GET /api/events/<id> and gets JSON back - no page reload.
  fetch(`/api/events/${form.dataset.eventId}`)
    .then((response) => response.json())
    .then((event) => {
      seatsLeft.textContent = event.seats_left;
      seatsInput.max = event.seats_left;
    })
    .catch(() => { /* keep the number rendered by the server */ });
}

// 3. Charts: one helper used by both summary pages.
//    stacked = true draws the datasets on top of each other (parts of one total).
function drawChart(canvasId, type, labels, datasets, stacked = false) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === "undefined") return;
  new Chart(canvas, {
    type: type,
    data: { labels: labels, datasets: datasets },
    options: {
      responsive: true,
      aspectRatio: type === "doughnut" ? 1.4 : 2,
      plugins: { legend: { position: "bottom" } },
      scales: type === "bar"
        ? { x: { stacked: stacked }, y: { stacked: stacked, beginAtZero: true } }
        : {},
    },
  });
}
