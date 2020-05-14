;(function () {
	$(".debug-link").on("click", function (event) {
		event.preventDefault()

		$(".landing-place-input").val($(this).text())
	})
})()
