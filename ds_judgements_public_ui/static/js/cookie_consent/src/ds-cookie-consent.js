import Data from "./data";
import dsCookieConsentBannerAPI from "./api/dsCookieConsentBannerAPI";

const getBannerElement = document.querySelector(Data.bannerWrapper.id);
const getCookieForm = document.querySelector(Data.formWrapper.id);
const getCookieObject = dsCookieConsentBannerAPI.getCookieValue(
  Data.cookies.cookieTwo
);
let measureRadioInput = document.querySelector(Data.form.analytics.measure);
let doNotMeasureRadioInput = document.querySelector(
  Data.form.analytics.doNotMeasure
);
let settingsRadioInput = document.querySelector(Data.form.settings.rememberSettings);
let doNotRememberSettingsRadioInput = document.querySelector(
  Data.form.settings.doNotRememberSettings
);

// Polyfill the remove() method IE9 and higher
// from:https://github.com/jserz/js_piece/blob/master/DOM/ChildNode/remove()/remove().md
(function (arr) {
  arr.forEach(function (item) {
    if (item.hasOwnProperty("remove")) {
      return;
    }
    Object.defineProperty(item, "remove", {
      configurable: true,
      enumerable: true,
      writable: true,
      value: function remove() {
        this.parentNode.removeChild(this);
      },
    });
  });
})([Element.prototype, CharacterData.prototype, DocumentType.prototype]);

// Treat DOM elements while the page is loading
(function () {
  // If the cookie dontShowCookieNotice exists
  // Hide the banner if visible
  if (dsCookieConsentBannerAPI.checkCookie(Data.cookies.cookieOne)) {
    if (getBannerElement) {
      getBannerElement.remove();
    }
  }

  if (getCookieForm) {
    // Update the state on the form radio elements
    // based on the cookie_policy value
    if (!dsCookieConsentBannerAPI.checkCookie(Data.cookies.cookieTwo)) {
      // Hide the banner if visible
      if (getBannerElement) {
        getBannerElement.remove();
      }
      doNotMeasureRadioInput.checked = true;
      doNotRememberSettingsRadioInput.checked = true;
    }

    if (getBannerElement) {
      getBannerElement.remove();
    }
  }
})();

// Create/delete cookies on page load
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    if (!dsCookieConsentBannerAPI.checkCookie(Data.cookies.cookieTwo)) {
      const cookieValue = {
        usage: false,
        settings: false,
        essential: true,
      };

      dsCookieConsentBannerAPI.setCookie(
        Data.cookies.cookieTwo,
        JSON.stringify(cookieValue),
        {
          "max-age": 90 * 24 * 60 * 60,
        }
      );

      // Delete GA cookies if cookies_policy cookie value is set to false
      Data.cookies.gaCookies.forEach((cookie) => {
        dsCookieConsentBannerAPI.deleteCookie(cookie);
      });
    } else {
      if (
        getCookieObject.hasOwnProperty("usage") &&
        getCookieObject.usage === false
      ) {
        Data.cookies.gaCookies.forEach((cookie) => {
          dsCookieConsentBannerAPI.deleteCookie(cookie);
        });
      }

      if (
        getCookieObject.hasOwnProperty("settings") &&
        getCookieObject.settings === false
      ) {
        Data.cookies.settings.forEach((cookie) => {
          dsCookieConsentBannerAPI.deleteCookie(cookie);
        });
      }

      // If Cookie Settings page
      // handle form state based on cookie_policy value / settings
      if (getCookieForm) {
        // Update the state on the form radio elements
        // based on the cookie_policy value
        if (
          getCookieObject.hasOwnProperty("usage") &&
          getCookieObject.usage === true &&
          !measureRadioInput.checked
        ) {
          measureRadioInput.checked = true;
        } else {
          doNotMeasureRadioInput.checked = true;
        }

        // Remove the functional cookies if the user hasn't consent
        if (
          getCookieObject.hasOwnProperty("settings") &&
          getCookieObject.settings === true &&
          !settingsRadioInput.checked
        ) {
          settingsRadioInput.checked = true;
        } else {
          doNotRememberSettingsRadioInput.checked = true;
        }
      }
    }
  });
})();

// Banner DOM implementation
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const oldCookieNotice = document.querySelector(
      Data.oldCookieBannerWrapper.class
    );
    const jsON = document.querySelector(Data.DOM.on);
    const jsOFF = document.querySelector(Data.DOM.off);

    // Display form elements if JS is enable
    if (jsON) {
      jsON.style.display = "block";
    }

    // Hide JS is not enabled message if JS is enabled
    if (jsOFF) {
      jsOFF.style.display = "none";
    }

    // Hide the old yellow Cookie banner for the MVP
    if (oldCookieNotice) {
      oldCookieNotice.remove();
    }

    // Check if cookie banner exists
    if (getBannerElement) {
      // Create Accept Optional Cookies
      dsCookieConsentBannerAPI.createButton(
        Data.buttonAccept.text,
        Data.buttonAccept.id,
        Data.buttonAccept.class,
      );

      // Create Reject Optional Cookies
      dsCookieConsentBannerAPI.createButton(
        Data.buttonReject.text,
        Data.buttonReject.id,
        Data.buttonReject.class,
      );

      // Select the buttons
      // !important - Do not move these above the DOM implementation
      const btnAccept = document.querySelector(`#${Data.buttonAccept.id}`);
      const btnReject = document.querySelector(`#${Data.buttonReject.id}`);
      const btnPreference = document.querySelector(Data.buttonPreferences.id);
      const bannerParagraph = document.querySelector(Data.bannerParagraph.id);
      const cookieHead = document.querySelector(Data.bannerHeadline.id);
      const getBannerElementContainer = getBannerElement.querySelector(
        ".container"
      );

      // Check if the button Accept Optional Cookies exists
      if (btnAccept) {
        // Binding to document (event delegation)
        btnAccept.addEventListener("click", (e) => {
          e.preventDefault();

          // Create dontShowCookieNotice cookie
          dsCookieConsentBannerAPI.setCookie(Data.cookies.cookieOne, "true", {
            "max-age": 90 * 24 * 60 * 60,
          });

          // Create/Update cookies_policy cookie
          dsCookieConsentBannerAPI.setCookie(
            Data.cookies.cookieTwo,
            '{"usage":true,"settings":true,"essential":true}',
            {
              "max-age": 90 * 24 * 60 * 60,
            }
          );

          dsCookieConsentBannerAPI.createButton(
            Data.hideThisMessage.text,
            Data.hideThisMessage.id,
            Data.hideThisMessage.class,
          );

          if (btnAccept) {
            btnAccept.remove();
          }

          if (btnReject) {
            btnReject.remove();
          }

          if (btnPreference) {
            btnPreference.remove();
          }

          if (cookieHead) {
            cookieHead.remove();
          }

          if (bannerParagraph) {
            bannerParagraph.innerHTML = Data.acceptMessageAfterInteraction.text;
            getBannerElementContainer.setAttribute(
              "aria-label",
              Data.acceptMessageAfterInteraction.ariaLabel
            );
          }

          // Get the Close This Message DOM element
          const hideThisMessage = document.querySelector(
            `#${Data.hideThisMessage.id}`
          );

          // If Close This Message DOM exists, hide banner
          if (hideThisMessage) {
            hideThisMessage.addEventListener("click", (e) => {
              e.preventDefault();
              // Hide the banner after Reject btn was clicked
              if (
                dsCookieConsentBannerAPI.checkCookie(Data.cookies.cookieOne)
              ) {
                if (getBannerElement) {
                  getBannerElement.remove();
                }
              }
            });
            bannerParagraph.focus();
          }

          // Add GA script and set the cookies at the client side
          const DOMhead = document.head;
          const gaScript = document.createElement("script");
          gaScript.id = "frontEndGA";
          gaScript.src =
            "https://nationalarchives.gov.uk/wp-content/plugins/ds-cookie-consent/dist/gtm-script.js";
          DOMhead.appendChild(gaScript);
        });
      }

      // Check if the button Reject Optional Cookies exists
      if (btnReject) {
        // Binding to document (event delegation)
        btnReject.addEventListener("click", (e) => {
          e.preventDefault();

          // Create dontShowCookieNotice cookie
          dsCookieConsentBannerAPI.setCookie(Data.cookies.cookieOne, "true", {
            "max-age": 90 * 24 * 60 * 60,
          });

          // Create/Update cookies_policy cookie
          dsCookieConsentBannerAPI.setCookie(
            Data.cookies.cookieTwo,
            '{"usage":false,"settings":false,"essential":true}',
            {
              "max-age": 90 * 24 * 60 * 60,
            }
          );

          dsCookieConsentBannerAPI.createButton(
            Data.hideThisMessage.text,
            Data.hideThisMessage.id,
            Data.hideThisMessage.class,
          );

          if (btnAccept) {
            btnAccept.remove();
          }

          if (btnReject) {
            btnReject.remove();
          }

          if (btnPreference) {
            btnPreference.remove();
          }

          if (cookieHead) {
            cookieHead.remove();
          }

          if (bannerParagraph) {
            bannerParagraph.innerHTML = Data.rejectMessageAfterInteraction.text;
            getBannerElementContainer.setAttribute(
              "aria-label",
              Data.rejectMessageAfterInteraction.ariaLabel
            );
          }

          // Get the Close This Message DOM element
          const hideThisMessage = document.querySelector(
            `#${Data.hideThisMessage.id}`
          );

          // If Close This Message DOM exists, hide banner
          if (hideThisMessage) {
            hideThisMessage.addEventListener("click", (e) => {
              e.preventDefault();
              // Hide the banner after Reject btn was clicked
              if (
                dsCookieConsentBannerAPI.checkCookie(Data.cookies.cookieOne)
              ) {
                if (getBannerElement) {
                  getBannerElement.remove();
                }
              }
            });
            bannerParagraph.focus();
          }

          const cookiesToUnset = [
            Data.cookiesToRemove.one,
            Data.cookiesToRemove.two,
            Data.cookiesToRemove.three,
            Data.cookiesToRemove.four,
            Data.cookiesToRemove.five
          ];

          // Unset GA cookies if available
          for (const cookie of cookiesToUnset) {
            if (dsCookieConsentBannerAPI.checkCookie(cookie)) {
              dsCookieConsentBannerAPI.deleteCookie(cookie);
            }
          }
        });
      }
    }
  });
})();
