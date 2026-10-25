// Mobile menu toggle
const menuBtn = document.getElementById("menuBtn"), nav = document.getElementById("nav");
if (menuBtn) menuBtn.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
});

// FAQ accordion: each button shows/hides its panel
document.querySelectorAll(".acc-btn").forEach(btn => btn.addEventListener("click", () => {
  const panel = document.getElementById(btn.getAttribute("aria-controls"));
  const open = btn.getAttribute("aria-expanded") === "true";
  btn.setAttribute("aria-expanded", String(!open));
  panel.hidden = open;
}));

// Questionnaire: client-side validation + "None of these" clears the others
const qForm = document.getElementById("qForm");
if (qForm) {
  const none = document.getElementById("noneBox");
  const boxes = qForm.querySelectorAll('input[name="symptoms"]');
  none.addEventListener("change", () => { if (none.checked) boxes.forEach(b => b.checked = false); });
  boxes.forEach(b => b.addEventListener("change", () => { if (b.checked) none.checked = false; }));
  qForm.addEventListener("submit", e => {
    const any = [...boxes].some(b => b.checked) || none.checked;
    document.getElementById("jsError").hidden = any;
    if (!any) e.preventDefault();
  });
}

// Feedback: live character counter
const msg = document.getElementById("message"), count = document.getElementById("count");
if (msg && count) { const upd = () => count.textContent = msg.value.length; msg.addEventListener("input", upd); upd(); }
