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

				/**
				 * @todo error to fix:

0|sociallydistanced  | SyntaxError: Unexpected token , in JSON at position 3
0|sociallydistanced  |     at JSON.parse (<anonymous>)
0|sociallydistanced  |     at /apps/sociallydistanced/backend/src/helpers/python.js:31:23
0|sociallydistanced  |     at PythonShell._endCallback (/apps/sociallydistanced/backend/node_modules/python-shell/index.js:218:20)
0|sociallydistanced  |     at terminateIfNeeded (/apps/sociallydistanced/backend/node_modules/python-shell/index.js:160:39)
0|sociallydistanced  |     at ChildProcess.<anonymous> (/apps/sociallydistanced/backend/node_modules/python-shell/index.js:133:13)
0|sociallydistanced  |     at ChildProcess.emit (events.js:310:20)
0|sociallydistanced  |     at Process.ChildProcess._handle.onexit (internal/child_process.js:275:12)

				 */
				//if (process.env.NODE_ENV == "development") {
				console.log(results)
				//}
				const json = JSON.parse(results)

				resolve(json)
			}
		)
	})
}
