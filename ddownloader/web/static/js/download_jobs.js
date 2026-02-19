/* Download jobs UI helpers: relative time + duration formatting.
 *
 * Expects:
 *  - <time class="js-rel-time" datetime="ISO">...</time>
 *  - <span class="js-duration" data-start="ISO" data-end="ISO">...</span>
 */

(function () {
  if (!window.Intl || !Intl.RelativeTimeFormat) return;
  const rtf = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" });

  function formatExact(date) {
    return date.toLocaleString(
      "en-US",
      {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric"
      }
    );
  }

  function formatRelative(date) {
    // past dates should be negative; future dates positive
    const seconds = Math.round((date.getTime() - Date.now()) / 1000);
    const abs = Math.abs(seconds);

    if (abs < 60) return rtf.format(seconds, "second");
    const minutes = Math.round(seconds / 60);
    if (Math.abs(minutes) < 60) return rtf.format(minutes, "minute");
    const hours = Math.round(minutes / 60);
    if (Math.abs(hours) < 24) return rtf.format(hours, "hour");
    const days = Math.round(hours / 24);
    if (Math.abs(days) < 30) return rtf.format(days, "day");
    const months = Math.round(days / 30);
    if (Math.abs(months) < 12) return rtf.format(months, "month");
    const years = Math.round(days / 365);
    return rtf.format(years, "year");
  }

  function formatDurationMillis(ms) {
    if (!Number.isFinite(ms) || ms < 0) return "—";

    const sec = Math.floor(ms / 1000);
    if (sec < 60) return `${sec} sec`;

    const min = Math.floor(sec / 60);
    if (min < 60) return `${min} min`;

    const hr = Math.floor(min / 60);
    if (hr < 24) return `${hr} hr`;

    const day = Math.floor(hr / 24);
    return `${day} day`;
  }

  function hydrateRelativeTimes() {
    for (const el of document.querySelectorAll('time.rel-time[datetime]')) {
      const iso = el.getAttribute('datetime');
      if (!iso) continue;

      const date = new Date(iso);
      if (Number.isNaN(date.getTime())) continue;

      el.textContent = `${formatRelative(date)}`;
    }
  }

  function hydrateDateTimes() {
    for (const el of document.querySelectorAll('time.fm-datetime[datetime]')) {
      const iso = el.getAttribute('datetime');
      if (!iso) continue;

      const date = new Date(iso);
      if (Number.isNaN(date.getTime())) continue;

      el.textContent = `${formatExact(date)}`;
    }
  }

  function hydrateDurations() {
    for (const el of document.querySelectorAll('.js-duration[data-start][data-end]')) {
      const startIso = el.getAttribute('data-start');
      const endIso = el.getAttribute('data-end');
      if (!startIso || !endIso) continue;

      const start = new Date(startIso);
      const end = new Date(endIso);
      if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) continue;

      el.textContent = formatDurationMillis(end.getTime() - start.getTime());
    }
  }

  function hydrate() {
    hydrateRelativeTimes();
    hydrateDurations();
  }

  hydrateDateTimes();
  hydrate();
  window.setInterval(hydrate, 30_000);
})();
