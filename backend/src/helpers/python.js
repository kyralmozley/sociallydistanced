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
		/**
		 * This is a really annoying hack, and is mainly a hotfix since the EC2
		 * instance requires we specify python3
		 */
		let py
		if (process.env.NODE_ENV == "development") {
			py = spawn("python", [pyMain, placeId])
		} else {
			py = spawn("python3", [pyMain, placeId])
		}

		py.stdout.on("data", (json) => {
			const object = JSON.parse(json)
			resolve(object)
		})

		py.stderr.on("data", (err) => {
			console.log(`Python Error: ${err}`)
			reject(err)
		})
	})
}
