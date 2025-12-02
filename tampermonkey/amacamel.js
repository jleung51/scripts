// ==UserScript==
// @name         Amacamel
// @namespace    https://github.com/jleung51/
// @downloadURL  https://raw.githubusercontent.com/jleung51/scripts/refs/heads/master/tampermonkey/amacamel.js
// @updateURL    https://raw.githubusercontent.com/jleung51/scripts/refs/heads/master/tampermonkey/amacamel.js
// @author       jleung51
// @version      2025-12-02
// @description  Shitty button which opens the item display page in CamelCamelCamel.
// @match        https://www.amazon.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=amazon.com
// @grant        GM_openInTab
// ==/UserScript==

(function() {
    'use strict';

    function addButton(text, onclick, styling) {
        styling = styling || {
          position: 'absolute',
          right: '3%',
          bottom: '75%',
          top: '20%',
          'z-index': 3
        };

        const button = document.createElement('button');
        document.body.appendChild(button);
        button.innerHTML = text;
        button.onclick = onclick;
        Object.keys(styling)
            .forEach(key => {
                button.style[key] = styling[key]
            });
        return button;
    }

    const url = window.location.href;
    if (url.match('.*/dp/.*')) {
        console.log('Amacamel: Display page detected.');
        const asin = url
            .replace(/https?\:\/\//, '')
            .replace(/(www\.)?amazon\.com.*\/dp\//, '')
            .replace(/\?.*/, ''); // Everything after the ASIN
        console.info(`Amacamel: Constructed ASIN ${asin}`);

        const camelUrl = `https://camelcamelcamel.com/product/${asin}`;
        addButton(
            'Camel Me',
            () => {
                GM_openInTab(camelUrl, {active: true});
            }
        );
    }

})();

