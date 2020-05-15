"use strict"

/**
 * Responsible for chart stuff
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
		lime: "#8eac34",
		lime_green: "#6BBC38",
		green: "#4fb373",
	}

	var labels = []
	for (var i = 0; i < 24; i++) {
		labels.push(i + ":00")
	}

	var chart = undefined
	function renderForecast(points) {
		var canvas = $(".result-graph")

		/**
		 * Destroy the current chart, if it exists
		 */
		if (chart != undefined) {
			chart.destroy()
		}

		var allZero = true
		var chart_colours = []
		for (i in points) {
			var point = points[i]

			if (point >= 1) {
				allZero = false
			}

			if (point < 10) {
				chart_colours[i] = colours.green
			} else if (point < 20) {
				chart_colours[i] = colours.lime_green
			} else if (point < 30) {
				chart_colours[i] = colours.lime
			} else if (point < 40) {
				chart_colours[i] = colours.yellow_lime
			} else if (point < 50) {
				chart_colours[i] = colours.yellow
			} else if (point < 60) {
				chart_colours[i] = colours.orange_yellow
			} else if (point < 70) {
				chart_colours[i] = colours.orange
			} else if (point < 80) {
				chart_colours[i] = colours.red_orange
			} else {
				chart_colours[i] = colours.red
			}
		}

		if (allZero) {
			return false
		}

		chart = new Chart(canvas[0], {
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

		return true
	}

	window.ctx_api = {
		renderForecast,
	}
})()
