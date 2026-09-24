"use strict";

document.querySelectorAll('[role="tablist"]').forEach((list) => {
  const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
  const select = (selected) => tabs.forEach((tab) => {
    const active = tab === selected;
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
    document.getElementById(tab.getAttribute("aria-controls")).hidden = !active;
  });
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (event) => {
      const positions = {ArrowRight: (index + 1) % tabs.length,
        ArrowLeft: (index - 1 + tabs.length) % tabs.length,
        Home: 0, End: tabs.length - 1};
      if (!(event.key in positions)) return;
      event.preventDefault();
      const target = tabs[positions[event.key]];
      select(target);
      target.focus();
    });
  });
});

const titles = {
  overview: "Ego-ExBind diagnostic protocol",
  retrieval: "Pair exposure and zero-shot retrieval",
  pmi: "PMI and zero-shot retrieval",
  binding: "Pair exposure and binding margins"
};
const dialog = document.getElementById("figure-dialog");
document.querySelectorAll("[data-figure]").forEach((button) => {
  button.addEventListener("click", () => {
    const name = button.dataset.figure;
    const source = button.parentElement.querySelector("img");
    document.getElementById("dialog-title").textContent = titles[name];
    const image = document.getElementById("dialog-image");
    image.src = source.src;
    image.alt = source.alt;
    dialog.showModal();
    document.body.classList.add("modal-open");
  });
});
document.getElementById("close-dialog").addEventListener("click", () => dialog.close());
dialog.addEventListener("close", () => document.body.classList.remove("modal-open"));
dialog.addEventListener("click", (event) => {
  const rect = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right ||
      event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
});

const sectionLinks = Array.from(document.querySelectorAll('.nav-links a[href^="#"]'));
const sections = sectionLinks.map((link) => document.querySelector(link.getAttribute("href")));
let framePending = false;
function updateNavigation() {
  const offset = document.querySelector(".site-header").offsetHeight + 80;
  let active = sections[0];
  sections.forEach((section) => {
    if (section.getBoundingClientRect().top <= offset) active = section;
  });
  sectionLinks.forEach((link) => {
    if (link.hash === `#${active.id}`) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
  framePending = false;
}
window.addEventListener("scroll", () => {
  if (!framePending) {
    framePending = true;
    requestAnimationFrame(updateNavigation);
  }
}, {passive: true});
updateNavigation();
