// One content page per language; only the colors change at night (local time).
(() => {
  function updateTheme() {
    const hour = new Date().getHours();
    document.documentElement.dataset.theme = hour >= 0 && hour < 5 ? 'dark' : 'light';
  }
  updateTheme();
  window.setInterval(updateTheme, 60000);
  window.addEventListener('pageshow', updateTheme);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) updateTheme();
  });
})();
