"use strict"

/**
 * @todo i need to re-write this from scratch
 */

/**
 * Limit scope -- helpful to stop interference
 */
;(function () {
	/**
	 * Browser-side cache
	 */
	var cache = {}

	/**
	 * Logs when we've sent feedback for a place
	 */
	var feedbacks = []

	/**
	 * Object containing string templates
	 */
	var strings = {
		prediction_prefix: "Current prediction: ",
		prediction_0: "1/5",
		prediction_1: "2/5",
		prediction_2: "3/5",
		prediction_3: "4/5",
		prediction_4: "5/5",

		description_closed: "This location seems to be closed",
		description_0: "You can safely social distance at this location",
		description_1: "You should be able to safely social distance at this location",
		description_2: "You may be able to safely social distance at this location",
		description_3: "It is unlikely that you will be able to safely social distance",
		description_4: "You cannot safely social distance at this location",

		queue_0: "It is unlikely that you will have to queue for entry",
		queue_1: "You may have to queue for entry",
		queue_2: "There is likely to be a short queue for entry",
		queue_3: "You will have to queue for entry",
		queue_4: "There is likely a long queue for entry",

		go_btn_default: "Go",
		go_btn_loading:
			'<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>' +
			"&nbsp;Loading...",

		error:
			'<div class="alert alert-danger mt-3" role="alert">Server Error. Please try again.</div>',
		no_place: '<div class="alert alert-info mt-3" role="alert">Please select a place.</div>',
	}

	var currentPlaceId = undefined
	var currentPlace = undefined

	/**
	 * Handles feedback
	 * @param {bool} isPositive If the feedback is 'Yes'
	 */
	function onFeedback(isPositive) {
		/**
		 * Prevent the same client from sending feedback to the same place multiple
		 * times. This is enforced on the server, but it's nice to have on the
		 * client too.
		 */
		if (feedbacks.includes(currentPlaceId)) return false

		if (isPositive) {
			// hide the feedback buttons
			$(".result-feedback-buttons").css("display", "none")
			$(".feedback-button").css("display", "none")
			$(".feedback-2-text").css("display", "none")

			// show the 'Thanks for your feedback!' text
			$(".result-feedback-thanks").removeClass("d-none")
			$(".result-feedback-2").removeClass("d-none")
			$(".result-feedback-thanks").css("display", "block")
			$(".result-feedback-2").css("display", "block")

			$.ajax({
				url: window.GLOBAL_ENV.API_BASE_URI + "/feedback/positive?placeId=" + currentPlaceId,
				crossDomain: true,
				method: "POST",
			})

			feedbacks.push(currentPlaceId)
		} else {
			$(".result-feedback-buttons").css("display", "none")
			$(".result-feedback-text").css("display", "none")
			$(".result-feedback-2").removeClass("d-none")
			$(".result-feedback-2").css("display", "block")
		}
	}

	function onFeedback2(level) {
		$(".result-feedback-thanks").removeClass("d-none")
		$(".feedback-button").css("display", "none")
		$(".feedback-2-text").css("display", "none")
		$(".result-feedback-text").css("display", "block")
		$(".result-feedback-thanks").css("display", "block")

		$.ajax({
			url:
				window.GLOBAL_ENV.API_BASE_URI +
				"/feedback/negative?placeId=" +
				currentPlaceId +
				"&level=" +
				level,
			crossDomain: true,
			method: "POST",
		})

		feedbacks.push(currentPlaceId)
	}

	function resetFeedbackButtons() {
		//$(".result-feedback-text").css("display", "block")
		//$(".result-feedback-buttons").css("display", "block")
		//$(".result-feedback-2").css("display", "none")
		//$(".result-feedback-thanks").css("display", "none")
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
		$("#sd--description").addClass("result-description-" + colour)
		$("#sd--description").text(description)
	}

	/**
	 * Utility function for showPrediction
	 * @private
	 * @param {string} description The text to show
	 * @param {string} colour The colour used in the class name
	 */
	function _setQueueDescription(description, colour) {
		// The ID selector *sucks*, but we don't really have a better option here
		$("#sd--queue").removeClass()
		$("#sd--queue").addClass("result-queue")
		$("#sd--queue").addClass("result-queue-" + colour)
		$("#sd--queue").text(description)
		$("#sd--queue").css("display", "block")
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
		$(".error-container").empty()

		// Reset feedback buttons, necessary as this is a SPA.
		resetFeedbackButtons()

		if (data.open) {
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
		} else {
			$(".result-prediction").text(strings.prediction_prefix)
			$("#sd--description").removeClass()
			$("#sd--description").addClass("result-description")
			$("#sd--description").addClass("bg-dark")
			$("#sd--description").addClass("text-white")
			$("#sd--description").text(strings.description_closed)
		}

		switch (data.queue) {
			case -1: {
				$(".result-queue").css("display", "none")
				break
			}

			case 0: {
				_setQueueDescription(strings.queue_0, "green")
				break
			}

			case 1: {
				_setQueueDescription(strings.queue_1, "lime")
				break
			}

			case 2: {
				_setQueueDescription(strings.queue_2, "yellow")
				break
			}

			case 3: {
				_setQueueDescription(strings.queue_3, "orange")
				break
			}

			case 4: {
				_setQueueDescription(strings.queue_4, "red")
				break
			}
		}

		currentPlaceId = data.placeId
		currentPlace = window.maps.thisPlace
		$(".result-title").text(currentPlace.name || currentPlace.formatted_address)

		try {
			if (window.ctx_api.renderForecast(data.graphPoints) == false) {
				$(".result-graph").css("display", "none")
			} else {
				$(".result-graph").css("display", "block")
			}
		} catch (err) {
			alert("Chart error: " + err)
			console.error(err)
		}

		$(".result-map").html(
			'<iframe width="100%" height="40%" frameborder="0" style="border:0" ' +
				'src="https://www.google.com/maps/embed/v1/place?q=place_id:' +
				data.placeId +
				"&key=" +
				window.GLOBAL_ENV.MAPS_API_KEY +
				'" allowfullscreen></iframe>'
		)

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
				error: function (data) {
					console.warn("Search request error: " + data)
					$(".landing-go-btn").html(strings.go_btn_default)
					$(".landing-go-btn").removeClass("disabled")
					$(".error-container").html(strings.error)
				},
			})
		}
	}

	/**
	 * Sets up events
	 */
	function setupEvents() {
		$(".landing-go-btn").on("click", function (event) {
			event.preventDefault()

			try {
				window.maps.updateAutocomplete()
			} catch (err) {
				console.warn("An error occurred:" + err)
			}

			var placeId = $(".landing-place-input").data("place_id")

			if (typeof placeId != "string") {
				$(".error-container").html(strings.no_place)
			} else {
				search(placeId)
			}
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
	})

	/**
	 * Expose an API for debugging
	 */
	window.sd_api = {
		showPrediction,
		search,
	}
})()
