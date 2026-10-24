// Two views of each paper: application illustration and method overview.
(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.paper-gallery').forEach(gallery => {
    const slides = [...gallery.querySelectorAll('.paper-slide')];
    const choices = [...gallery.querySelectorAll('.paper-choice')];
    const playback = gallery.querySelector('.paper-playback');
    let current = 0;
    let playing = !reducedMotion.matches;
    let visible = false;
    let hovered = false;
    const updatePlayback = () => {
      playback.textContent = playing ? 'Ⅱ' : '▶';
      playback.setAttribute('aria-label', playing ? gallery.dataset.pause : gallery.dataset.play);
      playback.title = playback.getAttribute('aria-label');
    };
    const show = index => {
      current = index;
      slides.forEach((slide, i) => { slide.hidden = i !== index; });
      choices.forEach((choice, i) => choice.setAttribute('aria-pressed', String(i === index)));
    };
    choices.forEach((choice, index) => {
      choice.addEventListener('click', () => {
        playing = false;
        show(index);
        updatePlayback();
      });
      choice.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? slides.length - 1 :
          (index + (event.key === 'ArrowRight' ? 1 : -1) + slides.length) % slides.length;
        choices[next].focus();
        choices[next].click();
      });
    });
    playback.addEventListener('click', () => { playing = !playing; updatePlayback(); });
    gallery.addEventListener('mouseenter', () => { hovered = true; });
    gallery.addEventListener('mouseleave', () => { hovered = false; });
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (visible) slides.forEach(slide => { slide.querySelector('img').loading = 'eager'; });
    }, { threshold: 0.15 });
    observer.observe(gallery);
    window.setInterval(() => {
      if (playing && visible && !hovered && !document.hidden && !gallery.contains(document.activeElement)) {
        show((current + 1) % slides.length);
      }
    }, 4000);
    reducedMotion.addEventListener('change', event => {
      if (event.matches) { playing = false; updatePlayback(); }
    });
    // Controls become available only when JavaScript is running.
    gallery.querySelector('.paper-gallery-controls').hidden = false;
    updatePlayback();
    show(0);
  });
})();
