/**
 * Responsible for chart stuff
 * @todo finish this -- it's not really done yet.
 */
;(function () {
	// Copied from scss/core/_variables.scss
	var colours = {
		red: "#e14a4e",
		red_orange: "#eb482b",
		orange: "#ee8632",
		orange_yellow: "#ffb624",
		yellow: "#f7c117",
		yellow_lime: "#E5F64D",
		lime: "#9cbd38",
		lime_green: "#6BBC38",
		green: "#4fb373",
	}

	var labels = []
	for (var i = 0; i < 24; i++) {
		labels.push(i + ":00")
	}

	function renderForecast(points) {
		var canvas = $(".result-graph")

		// Debugging
		alert(points.length)

		var chart_colours = []
		for (i in points) {
			var point = points[i]
			if (point < 15) {
				chart_colours[i] = colours.green
			} else if (point < 35) {
				chart_colours[i] = colours.lime
			} else if (point < 55) {
				chart_colours[i] = colours.yellow
			} else if (point < 75) {
				chart_colours[i] = colours.orange
			} else {
				chart_colours[i] = colours.red
			}
		}

		console.log("Chart colours", chart_colours)
		console.log("Points", points)

		var myChart = new Chart(canvas, {
			type: "bar",
			data: {
				labels,
				datasets: [
					{
						label: "Prediction",
						backgroundColor: chart_colours,
						data: points,
					},
				],
			},
			options: {
				legend: {
					display: false,
				},
				scales: {
					y: {
						min: 0,
						max: 100,
						stepSize: 1,
						display: false,
					},
					yAxes: {
						gridLines: {
							display: false,
						},
						ticks: {
							callback: function (value) {
								return value * 100 + "%" // convert it to percentage
							},
						},
					},
					xAxes: {
						gridLines: {
							display: false,
						},
					},
				},
			},
		})
	}

	window.ctx_api = {
		renderForecast,
	}
})()
