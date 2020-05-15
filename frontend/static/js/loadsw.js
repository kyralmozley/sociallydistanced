"use strict"

/**
 * I still hate service workers.
 * Some of this code was copied/pasted from:
 * https://css-tricks.com/serviceworker-for-offline/
 */
;(function () {
	// ServiceWorker is a progressive technology. Ignore unsupported browsers
	if ("serviceWorker" in navigator) {
		console.log("CLIENT: service worker registration in progress.")
		navigator.serviceWorker.register("/sw.js").then(
			function () {
				console.log("CLIENT: service worker registration complete.")
			},
			function () {
				console.log("CLIENT: service worker registration failure.")
			}
		)
	} else {
		console.log("CLIENT: service worker is not supported.")
	}
})()
