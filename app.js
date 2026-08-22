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

  /* ---- keep the screen awake while cooking ----
     On both pages, and remembered between them: a page navigation drops the
     lock the same way switching apps does, and you move between the plan and
     the recipes constantly while cooking. `wanted` is the choice; `lock` is
     whether we currently hold one. Keeping them separate is what lets us take
     the lock back after the browser takes it away. */
  var wakeBtn = document.getElementById('wake');
  if (wakeBtn) {
    if (!('wakeLock' in navigator)) {
      wakeBtn.hidden = true;
    } else {
      var WAKE_KEY = 'sk-wake-v1';
      var lock = null;
      var wanted = false;
      try { wanted = localStorage.getItem(WAKE_KEY) === '1'; } catch (e) { wanted = false; }

      var paint = function () {
        wakeBtn.setAttribute('aria-pressed', String(wanted));
      };

      var remember = function () {
        try { localStorage.setItem(WAKE_KEY, wanted ? '1' : '0'); } catch (e) {}
      };

      var release = function () {
        if (!lock) return;
        var l = lock;
        lock = null;
        l.release().catch(function () {});
      };

      // Only NotSupportedError means this device will never do it — hide the
      // button for good. Everything else is transient: NotAllowedError fires
      // simply because the page wasn't visible at that instant, and hiding the
      // button on that would delete the feature until a reload. Reset the
      // toggle so the UI isn't lying, and leave the button there to retry.
      var acquire = function (silent) {
        return navigator.wakeLock.request('screen').then(function (l) {
          lock = l;
          l.addEventListener('release', function () { lock = null; });
        }).catch(function (e) {
          if (e && e.name === 'NotSupportedError') {
            wanted = false;
            remember();
            paint();
            wakeBtn.hidden = true;
            return;
          }
          if (!silent) { wanted = false; remember(); paint(); }
        });
      };

      wakeBtn.addEventListener('click', function () {
        wanted = !wanted;
        remember();
        paint();
        if (wanted) { acquire(false); } else { release(); }
      });

      // iOS drops the lock when you switch apps, and any navigation drops it too.
      // Take it back whenever the page is visible and the choice is still on.
      document.addEventListener('visibilitychange', function () {
        if (document.visibilityState === 'visible' && wanted && !lock) acquire(true);
      });

      paint();
      if (wanted) acquire(true);
    }
  }


  /* ---- show one prep track at a time ---- */
  var picks = document.querySelectorAll('.track-pick button');
  var tracks = document.querySelector('.tracks');
  if (picks.length && tracks) {
    picks.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var want = btn.dataset.track;
        picks.forEach(function (b) {
          b.setAttribute('aria-pressed', String(b === btn));
        });
        tracks.classList.remove('only-wet', 'only-dry');
        if (want !== 'both') tracks.classList.add('only-' + want);
      });
    });
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
