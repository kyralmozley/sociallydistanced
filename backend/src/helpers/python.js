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
	return new Promise((resolve, reject) => {
		PythonShell.run(
			script,
			{
				mode: "text",
				args,
				scriptPath: pyRoot,
			},
			(err, results) => {
				if (err) {
					console.error(err)
					return reject(err)
				}

				if (process.env.NODE_ENV == "development") {
					console.log(results)
				}
				const json = JSON.parse(results)

				resolve(json)
			}
		)
	})
}
