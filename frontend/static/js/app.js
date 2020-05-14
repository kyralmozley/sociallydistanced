/**
 * Limit scope -- helpful to stop interference
 * This code *cannot* use non-ES6 features. This is to support legacy devices.
 */
;(function () {
	/**
	 * Browser-side cache
	 */
	var cache = {}

	/**
	 * Object containing string templates
	 */
	var strings = {
		prediction_prefix: "Current prediction: ",
		prediction_0: "1",
		prediction_1: "2",
		prediction_2: "3",
		prediction_3: "4",
		prediction_4: "5",

		description_0: "You can safely social distance at this location",
		description_1: "You should be able to safely social distance at this location",
		description_2: "You can probably safely social distance at this location",
		description_3: "It is unlikely that you will be able to safely social distance",
		description_4: "You cannot safely social distance at this location",

		go_btn_default: "Go",
		go_btn_loading:
			'<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>' +
			"&nbsp;Loading...",

		error: '<div class="alert alert-danger mt-3" role="alert">Server Error. Please try again.</div>'
	}

	/**
	 * Handles feedback
	 * @param {bool} isPositive If the feedback is 'Yes'
	 */
	function onFeedback(isPositive) {
		/**
		 * @todo send feedback to the server
		 */
		if (isPositive) {
			// hide the feedback buttons
			$(".result-feedback-buttons").css("display", "none")
			$(".feedback-button").css("display", "none")
			$(".feedback-2-text").css("display", "none")

			// show the 'Thanks for your feedback!' text
			$(".result-feedback-thanks").removeClass("d-none")
			$(".result-feedback-2").removeClass("d-none")
		} else {
			$(".result-feedback-buttons").css("display", "none")
			$(".result-feedback-2").removeClass("d-none")
			$(".result-feedback-text").css("display", "none")
		}
	}

	function onFeedback2(level) {
		$(".feedback-button").css("display", "none")
		$(".result-feedback-thanks").removeClass("d-none")
		$(".feedback-2-text").css("display", "none")
		$(".result-feedback-text").css("display", "block")

		/**
		 * @todo send to server
		 */
	}

	/**
	 * Utility function for showPrediction
	 * @private
	 * @param {string} description The text to show
	 * @param {string} colour The colour used in the class name
	 */
	function _setPredictionDescription(description, colour) {
		// The ID selector *sucks*, but we don't really have a better option here
		$("#sd--description").removeClass()
		$("#sd--description").addClass("result-description")
		$("#sd--description").addClass("sd-ta-center")
		$("#sd--description").addClass("result-description-" + colour)
		$("#sd--description").text(description)
	}

	/**
	 * Renders the data on the page
	 * @param {Object} data See implementation notes for format
	 *
	 * @structure for data:
	 * {
	 * 		prediction: 0-4,
	 * 		graphPoints: (24 data points in an array; data points ranging from 0-4),
	 * 		placeId: (Google Maps place ID)
	 * }
	 */
	function showPrediction(data) {
		switch (data.prediction) {
			case 0: {
				$(".result-prediction").text(strings.prediction_prefix + strings.prediction_0)
				_setPredictionDescription(strings.description_0, "green")
				break
			}

			case 1: {
				$(".result-prediction").text(strings.prediction_prefix + strings.prediction_1)
				_setPredictionDescription(strings.description_1, "lime")
				break
			}

			case 2: {
				$(".result-prediction").text(strings.prediction_prefix + strings.prediction_2)
				_setPredictionDescription(strings.description_2, "yellow")
				break
			}

			case 3: {
				$(".result-prediction").text(strings.prediction_prefix + strings.prediction_3)
				_setPredictionDescription(strings.description_3, "orange")
				break
			}

			case 4: {
				$(".result-prediction").text(strings.prediction_prefix + strings.prediction_4)
				_setPredictionDescription(strings.description_4, "red")
				break
			}
		}

		$(".result-title").text("Place ID: " + data.placeId)

		/**
		 * @todo map and graph (chart.js)
		 */

		$(".result").css("display", "block")
		$(".result").removeClass("d-none")
		$(".landing").css("display", "none")
	}

	/**
	 * Searches for a place
	 * @param {String} placeId Google Maps API place ID
	 */
	function search(placeId) {
		if (typeof cache[placeId] == "object") {
			$(".landing-go-btn").html(strings.go_btn_default)
			$(".landing-go-btn").removeClass("disabled")
			showPrediction(cache[placeId])
		} else {
			$(".landing-go-btn").html(strings.go_btn_loading)
			$(".landing-go-btn").addClass("disabled")

			$.ajax({
				url: window.GLOBAL_ENV.API_BASE_URI + "/main/place?placeId=" + placeId,
				crossDomain: true,
				success: function (data) {
					$(".landing-go-btn").html(strings.go_btn_default)
					$(".landing-go-btn").removeClass("disabled")
					showPrediction(data)
					cache[placeId] = data
				},
				error: function(data) {
					$(".landing-go-btn").html(strings.go_btn_default)
					$(".landing-go-btn").removeClass("disabled")
					$(".error-container").html(strings.error)
				}
			})
		}
	}

	/**
	 * Sets up events
	 */
	function setupEvents() {
		$(".landing-go-btn").on("click", function (event) {
			event.preventDefault()
			var placeId = $(".landing-place-input").val()
			search(placeId)
		})

		$(".result-feedback-positive").on("click", function (event) {
			event.preventDefault()
			onFeedback(true)
		})

		$(".result-feedback-negative").on("click", function (event) {
			event.preventDefault()
			onFeedback(false)
		})

		$(".feedback-button").on("click", function (event) {
			event.preventDefault()
			onFeedback2($(this).data("level"))
		})

		$(".back-link").on("click", function (event) {
			event.preventDefault()
			$(".result").css("display", "none")
			$(".landing").css("display", "block")
		})
	}

	/**
	 * Shows the landing page
	 */
	function showLandingPage() {
		$(".landing").css("display", "block")
		$(".landing").removeClass("d-none")
	}

	/**
	 * Init function calls
	 */
	$(function () {
		setupEvents()
		showLandingPage()
		console.log("Loaded!")
	})

	/**
	 * Expose an API for debugging
	 */
	window.sd_api = {
		showPrediction,
	}
})()
