// ==UserScript==
// @name        Tving Hack
// @include     /^https?:\/\/[^/]*(tving)[^/]*\/.*$/
// ==/UserScript==
const pathname = window.location.href;
const isTving = pathname.includes("tving");

//티빙자동 로그인
(function() {
  'use strict';
  if (!isTving) return;
  if (pathname.includes("onboarding")) window.location.href = 'https://www.tving.com/account/login/tving?returnUrl=https://www.tving.com/live/C00551';

  const userId = 'enbita';
  const userPassword = 'qpwpeprp1!';

  function setReactInput(input, value) {
      const nativeSetter = Object.getOwnPropertyDescriptor(input.__proto__, 'value').set;
      nativeSetter.call(input, value);
      input.dispatchEvent(new Event('input', { bubbles: true }));
  }

  function fillFormAndLogin() {
      const idInput = document.querySelector('input[name="id"]');
      const pwInput = document.querySelector('input[name="password"]');
      const autoLoginBtn = document.getElementById('autoLoginCheckbox');

      if (idInput && pwInput && autoLoginBtn) {
          setReactInput(idInput, userId);
          setReactInput(pwInput, userPassword);

          if (autoLoginBtn.getAttribute('aria-checked') === 'false') {
              autoLoginBtn.click();
          }

          const loginBtn = Array.from(document.querySelectorAll('button[type="submit"]'))
              .find(btn => btn.innerText.includes('로그인하기'));
          if (loginBtn) loginBtn.click();
          console.log('자동 로그인 시도 완료');
      }
  }

  function clickFullscreenButton() {
      const fullscreenBtn = document.querySelector('button.con__fullscreen[aria-label="전체화면"]');
      if (fullscreenBtn) {
          fullscreenBtn.click();
          console.log('전체화면 버튼 클릭 완료');
      }
  }

  const loginObserver = new MutationObserver((mutations, obs) => {
      const idInput = document.querySelector('input[name="id"]');
      const pwInput = document.querySelector('input[name="password"]');
      const autoLoginBtn = document.getElementById('autoLoginCheckbox');

      if (idInput && pwInput && autoLoginBtn) {
          // 3초 후 로그인 실행
          setTimeout(() => {
              fillFormAndLogin();
          }, 3000);

          obs.disconnect(); // 중복 실행 방지
      }
  });

  loginObserver.observe(document.body, { childList: true, subtree: true });


})();

//티빙 자동 전체화면
(function() {
  if (!isTving) return;
  // 전체화면 버튼 감지
  const fullscreenObserver = new MutationObserver((mutations, obs) => {
      const fullscreenBtn = document.querySelector('button.con__fullscreen[aria-label="전체화면"]');
      if (fullscreenBtn) {
          clickFullscreenButton();
          obs.disconnect();
      }
  });
  fullscreenObserver.observe(document.body, { childList: true, subtree: true });
})();

//티빙 자동 소리 켜기
(function() {
  if (!isTving) return;
  const soundButtonInterval = setInterval(() => {
    // 버튼 내부 span 텍스트로 식별
    const soundBtn = Array.from(document.querySelectorAll('button'))
        .find(btn => btn.innerText.includes('클릭하여 소리켜기'));

    if (soundBtn) {
        soundBtn.click();
        console.log('소리 켜기 버튼 클릭 완료');
        clearInterval(soundButtonInterval);
    }
}, 500);


})();

//티빙 자동 광고 건너뛰기
(function() {
  if (!isTving) return;

  let adSkipTimeout = null;
  const adSkipInterval = setInterval(() => {
      const adBtn = Array.from(document.querySelectorAll('button.ad-skip-btn'))
          .find(btn => btn.innerText.includes('광고 건너뛰기'));

      if (adBtn && !adSkipTimeout) {
          adSkipTimeout = setTimeout(() => {
              adBtn.click();
              console.log('광고 건너뛰기 버튼 클릭 완료');
              adSkipTimeout = null;
          }, 500);
      }
  }, 1000);



})();

//티빙 자동 요소 삭제
(function () {
  'use strict';
  if (!isTving) return;

  const GRID_AREA_CLASSES = [
      '[grid-area:meta-area]',
      '[grid-area:left-area]',
      '[grid-area:band-area]',
      '[grid-area:right-area]'
  ];

  function removeTargets() {


      // footer
      document
          .querySelectorAll('footer.layout-container')
          .forEach(el => el.remove());

      // section (grid-area class)
      GRID_AREA_CLASSES.forEach(cls => {
          const selector = '.' + CSS.escape(cls);
          document.querySelectorAll(selector).forEach(el => {
              el.remove();
          });
      });
  }

  // 최초 실행
  removeTargets();

  // SPA 대응
  const observer = new MutationObserver(removeTargets);
  observer.observe(document.documentElement, {
      childList: true,
      subtree: true
  });
})();
