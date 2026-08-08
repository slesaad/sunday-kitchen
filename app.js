/* Sunday Kitchen — small progressive enhancements. Nothing here is required
   for the pages to work; if JS is off you still get every recipe. */

(function () {
  'use strict';

  /* ---- expand / collapse all recipes ---- */
  document.querySelectorAll('[data-all]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.dataset.all === 'open';
      document.querySelectorAll('.recipe details').forEach(function (d) {
        d.open = open;
      });
    });
  });

  /* ---- open a recipe when linked to directly (#slug) ---- */
  function openTarget() {
    var id = location.hash.slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.classList.contains('recipe')) {
      var d = el.querySelector('details');
      if (d) d.open = true;
      el.scrollIntoView();
    }
  }
  openTarget();
  window.addEventListener('hashchange', openTarget);

  /* ---- keep the screen awake while cooking ---- */
  var wakeBtn = document.getElementById('wake');
  if (wakeBtn) {
    if (!('wakeLock' in navigator)) {
      wakeBtn.hidden = true;
    } else {
      var lock = null;

      var release = function () {
        if (lock) { lock.release(); lock = null; }
        wakeBtn.setAttribute('aria-pressed', 'false');
      };

      var acquire = function () {
        return navigator.wakeLock.request('screen').then(function (l) {
          lock = l;
          wakeBtn.setAttribute('aria-pressed', 'true');
          l.addEventListener('release', function () {
            lock = null;
            wakeBtn.setAttribute('aria-pressed', 'false');
          });
        }).catch(function () {
          wakeBtn.hidden = true;
        });
      };

      wakeBtn.addEventListener('click', function () {
        if (lock) { release(); } else { acquire(); }
      });

      // iOS drops the lock when you switch apps — take it back on return.
      document.addEventListener('visibilitychange', function () {
        if (document.visibilityState === 'visible' &&
            wakeBtn.getAttribute('aria-pressed') === 'true' && !lock) {
          acquire();
        }
      });
    }
  }

  /* ---- shopping list, remembered on this device ---- */
  var boxes = document.querySelectorAll('.shop input[type="checkbox"]');
  if (boxes.length) {
    var KEY = 'sk-shop-v1';
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }

    boxes.forEach(function (box) {
      var id = box.closest('label').textContent.trim().slice(0, 60);
      if (saved[id]) box.checked = true;
      box.addEventListener('change', function () {
        if (box.checked) { saved[id] = 1; } else { delete saved[id]; }
        try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* private mode */ }
      });
    });

    var clear = document.getElementById('clear-shop');
    if (clear) {
      clear.addEventListener('click', function () {
        boxes.forEach(function (b) { b.checked = false; });
        saved = {};
        try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
      });
    }
  }
})();
