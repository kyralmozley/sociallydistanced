"use strict"
;(function () {
	// Create the search box and link it to the UI element.
	var input = $(".landing-place-input")
	var searchBox = new google.maps.places.SearchBox(input[0])

	// Listen for the event fired when the user selects a prediction and retrieve
	// more details for that place.
	searchBox.addListener("places_changed", updateAutocomplete)

	function updateAutocomplete() {
		var places = searchBox.getPlaces()

		if (places.length == 0) {
			return console.log("No places")
		}

		// Get the first place (ID 0)
		const place = places[0]
		//input.val(typeof place.name == "string" ? place.name : place.formatted_address)
		input.data("place_id", place.place_id)

		window.maps.thisPlace = place

		window.sd_api.search(place.place_id)
	}

	window.maps = window.maps || {}
	window.maps.updateAutocomplete = updateAutocomplete
})()
