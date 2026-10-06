/*
  Main UI Interactions
  --------------------
  Safe to keep as static JS in Django.
  Suggested Django path later: static/js/main.js
*/

// Move the decorative glow with the mouse pointer on devices that support hover.
const cursorGlow = document.querySelector('[data-cursor-glow]');

if (cursorGlow && window.matchMedia('(hover: hover)').matches) {
  window.addEventListener('pointermove', (event) => {
    cursorGlow.style.left = `${event.clientX}px`;
    cursorGlow.style.top = `${event.clientY}px`;
  });
}

// Mobile navigation toggle.
const menuButton = document.querySelector('[data-menu-button]');
const mainNav = document.querySelector('[data-main-nav]');

if (menuButton && mainNav) {
  menuButton.addEventListener('click', () => {
    const isOpen = mainNav.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
}

// Add active class to the current navigation item.
const currentPath = window.location.pathname;

document.querySelectorAll('[data-nav]').forEach((link) => {
  const linkPath = new URL(link.getAttribute('href'), window.location.origin).pathname;

  if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
    link.classList.add('active');
  }
});

// Reveal elements when they enter the viewport.
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

// Small 3D card movement on desktop only.
if (window.matchMedia('(hover: hover)').matches) {
  document.querySelectorAll('[data-tilt-card]').forEach((card) => {
    card.addEventListener('mousemove', (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;

      card.style.transform = `translateY(-10px) rotateX(${y * -4}deg) rotateY(${x * 4}deg)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}

// Keep footer year dynamic.
document.querySelectorAll('[data-year]').forEach((target) => {
  target.textContent = new Date().getFullYear();
});
