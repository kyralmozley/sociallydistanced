/**
 * Responsible for chart stuff
 * @todo finish this -- it's not really done yet.
 */
;(function () {
	var labels = []
	for (var i = 0; i < 24; i++) {
		labels.push(i + ":00")
	}

	function renderForecast(points) {
		var canvas = $(".result-graph")

		/*
		var myChart = new Chart(canvas, {
			type: "line",
			data: {
				datasets: [
					{
						label: "Prediction",
						data: points,
						borderWidth: 1,
					},
				],
			},
		})
		*/

		var myChart = new Chart(canvas, {
			type: "bar",
			data: {
				labels,
				datasets: [
					{
						label: "Prediction",
						data: points,
						barPercentage: 1,
						backgroundColor: [
							"rgba(255, 99, 132, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(255, 206, 86, 1)",
							"rgba(75, 192, 192, 1)",
							"rgba(153, 102, 255, 01)",
							"rgba(255, 159, 64, 1)",
						],
						borderColor: [
							"rgba(255, 99, 132, 1)",
							"rgba(54, 162, 235, 1)",
							"rgba(255, 206, 86, 1)",
							"rgba(75, 192, 192, 1)",
							"rgba(153, 102, 255, 1)",
							"rgba(255, 159, 64, 1)",
						],
						borderWidth: 1,
					},
				],
			},
			options: {
				scaleOverride: true,
				scaleSteps: 10,
				scaleStepWidth: 50,
				scaleStartValue: 0,

				responsive: true,
				maintainAspectRatio: true,
				legend: {
					display: false,
				},
				scales: {
					yAxes: [
						{
							ticks: {
								max: 5,
							},
						},
					],
				},
			},
		})
	}

	window.ctx_api = {
		renderForecast,
	}
})()
