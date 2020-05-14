const fs = require("fs")
const path = require("path")
const { spawn } = require("child_process")

const pyMain = path.join(__dirname, "..", "..", "..", "ml", "main.py")

/**
 * Runs the main.py script
 * @param {string} placeId The Google Maps API place ID
 * @returns Promise<resolve: Object data, reject: error>
 */
module.exports = (placeId) => {
	return new Promise((resolve, reject) => {
		console.log(pyMain, placeId)
		const py = spawn("python", [pyMain, placeId])

		py.stdout.on("data", (json) => {
			console.log("JSON", json, "PARSED", json.toString())
			const object = JSON.parse(json)
			console.log(object)
			resolve(object)
		})

		py.stderr.on("data", (err) => {
			console.log("ERROR", err.toString())
			reject(err)
		})

		py.stderr.on("close", (code) => {
			console.log(`Process quit with code: ${code}`)
		})
	})
}
