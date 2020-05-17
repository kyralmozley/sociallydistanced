"use strict"

const path = require("path")
const { PythonShell } = require("python-shell")

const pyRoot = path.join(__dirname, "..", "..", "..", "ml")

/**
 * Runs the main.py script
 * @param {string} placeId The Google Maps API place ID
 * @returns Promise<resolve: Object data, reject: error>
 */
module.exports = (script, args) => {
	console.log(1)
	return new Promise((resolve, reject) => {
		console.log(2)
		PythonShell.run(
			script,
			{
				mode: "text",
				args,
				scriptPath: pyRoot,
			},
			(err, results) => {
				console.log(3)
				if (err) {
					console.error(err)
					return reject(err)
				}

				try {
					console.log(results)
					if (process.env.NODE_ENV == "development") {
						console.log(results[0])
					}
					const json = JSON.parse(results[0])

					resolve(json)
				} catch (err) {
					console.error(err)
					reject(err)
				}
			}
		)
	})
}
