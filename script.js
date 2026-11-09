'use strict';
const rows = [...document.querySelectorAll('.moment-table tbody tr')];
const search = document.querySelector('#search');
let wording = 'all';
const filterButtons = [...document.querySelectorAll('[data-filter]')];
document.querySelector('.controls').hidden = false;
function filterRows() {
  const query = search.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const row of rows) {
    const visible = (wording === 'all' || row.dataset.kind === wording) && row.textContent.toLocaleLowerCase().includes(query);
    row.hidden = !visible;
    if (visible) count++;
  }
  document.querySelector('#result-count').textContent = `${count} moment${count === 1 ? '' : 's'}`;
  document.querySelector('#empty').hidden = count !== 0;
}
search.addEventListener('input', filterRows);
filterButtons.forEach(button => button.addEventListener('click', () => {
  wording = button.dataset.filter;
  filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  filterRows();
}));
// A small tribute to the old responsive-web Easter eggs. Width changes only:
// mobile browser toolbars changing height should not send yarn flying.
const wool = document.querySelector('#wool');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let lastWidth = window.innerWidth, resizeTimer, rolling = false, direction = 1;
function rollWool() {
  if (rolling || reducedMotion.matches || typeof wool.animate !== 'function') return;
  rolling = true;
  const size = wool.offsetWidth, travel = window.innerWidth + size * 3;
  const start = direction > 0 ? -size * 1.5 : window.innerWidth + size;
  const finish = direction > 0 ? window.innerWidth + size : -size * 1.5;
  const turns = direction * travel / (Math.PI * size) * 360;
  const animation = wool.animate([
    {transform:`translateX(${start}px) rotate(0deg)`},
    {transform:`translateX(${finish}px) rotate(${turns}deg)`}
  ], {duration: Math.min(4000, Math.max(2300, travel * 2.3)), easing:'cubic-bezier(.2,.6,.4,1)'});
  animation.onfinish = animation.oncancel = () => { rolling = false; };
  direction *= -1;
}
window.addEventListener('resize', () => {
  const width = window.innerWidth;
  if (Math.abs(width - lastWidth) < 3) return;
  lastWidth = width;
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(rollWool, 140);
});
