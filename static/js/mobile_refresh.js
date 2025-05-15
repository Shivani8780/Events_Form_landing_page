document.addEventListener('DOMContentLoaded', function () {
  let isRefreshing = false;
  let startY = 0;
  let currentY = 0;
  let threshold = 100; // Pull down distance in px to trigger refresh
  let refreshIndicator = document.createElement('div');

  refreshIndicator.style.position = 'fixed';
  refreshIndicator.style.top = '0';
  refreshIndicator.style.left = '0';
  refreshIndicator.style.right = '0';
  refreshIndicator.style.height = '50px';
  refreshIndicator.style.backgroundColor = '#1d4e89';
  refreshIndicator.style.color = 'white';
  refreshIndicator.style.display = 'flex';
  refreshIndicator.style.justifyContent = 'center';
  refreshIndicator.style.alignItems = 'center';
  refreshIndicator.style.fontSize = '18px';
  refreshIndicator.style.zIndex = '9999';
  refreshIndicator.style.transform = 'translateY(-50px)';
  refreshIndicator.style.transition = 'transform 0.3s ease';
  refreshIndicator.textContent = 'Refreshing...';
  document.body.appendChild(refreshIndicator);

  function showRefreshIndicator() {
    refreshIndicator.style.transform = 'translateY(0)';
  }

  function hideRefreshIndicator() {
    refreshIndicator.style.transform = 'translateY(-50px)';
  }

  window.addEventListener('touchstart', function (e) {
    if (window.scrollY === 0) {
      startY = e.touches[0].pageY;
      currentY = startY;
    }
  });

  window.addEventListener('touchmove', function (e) {
    currentY = e.touches[0].pageY;
    if (window.scrollY === 0 && currentY - startY > threshold && !isRefreshing) {
      isRefreshing = true;
      showRefreshIndicator();
      setTimeout(function () {
        location.reload();
      }, 500);
    }
  });

  window.addEventListener('touchend', function () {
    if (!isRefreshing) {
      hideRefreshIndicator();
    }
  });
});
