
const root = document.documentElement;
const themeRoot = document.querySelector('.theme-root') || root;
const toggle = document.getElementById('theme-toggle');
const storageKey = 'site-theme';

function applyTheme(name) {
  if (!themeRoot) return;
  if (name === 'dark') themeRoot.setAttribute('data-theme', 'dark');
  else themeRoot.removeAttribute('data-theme');
  if (toggle) toggle.textContent = name === 'dark' ? '☀️' : '🌙';
}

function initTheme() {
  const saved = localStorage.getItem(storageKey);
  if (saved) { applyTheme(saved); return }
  const prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(prefers ? 'dark' : 'light');
}

if (toggle) {
  toggle.addEventListener('click', function () {
    const current = localStorage.getItem(storageKey) === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(storageKey, next);
    applyTheme(next);
  });
}

initTheme();



const links = document.querySelectorAll('.main-nav a');
const path = location.pathname;
links.forEach(a => { if (a.getAttribute('href') === path) a.classList.add('active') });



function applyCodeFeatures() {
  document.querySelectorAll('pre code').forEach(block => {
    hljs.highlightElement(block);
    hljs.lineNumbersBlock(block);

    copy_svg = '<svg viewBox="0 0 24 24" width="18" height="18" class="copyButtonIcon_y97N"><path fill="currentColor" d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"></path></svg>';
    copied_svg = '<svg viewBox="0 0 24 24" width="18" height="18" class="copyButtonSuccessIcon_LjdS"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"></path></svg>';

    if (!block.parentElement.querySelector('.copy-btn')) {
      const btn = document.createElement('button');
      btn.innerHTML = copy_svg
      btn.className = 'copy-btn';
      block.parentElement.prepend(btn);

      const clipboard = new ClipboardJS(btn, {
        target: () => block
      });

      clipboard.on('success', () => {
        btn.innerHTML = copied_svg
        setTimeout(() => btn.innerHTML = copy_svg, 1000);
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', applyCodeFeatures);



const menuToggle = document.getElementById('menu-toggle');
const mainNav = document.querySelector('.main-nav');
const menuOverlay = document.getElementById('menu-overlay');
    console.log('asd')

function openMenu() {
    mainNav.classList.add('active');
    menuOverlay.style.display = 'block';
}

function closeMenu() {
    mainNav.classList.remove('active');
    menuOverlay.style.display = 'none';
}

menuToggle.addEventListener('click', () => {
    console.log('click')
    if(mainNav.classList.contains('active')) {
        closeMenu();
    } else {
        openMenu();
    }
});

menuOverlay.addEventListener('click', closeMenu);