const express = require("express")
const morgan = require("morgan")
const bodyParser = require("body-parser")
const config = require("../config")
const routes = require("../api")

/**
 * Initializes express
 * Intended to be used by the loaders index.js
 * @returns {ExpressApp} The express app
 */
module.exports = async () => {
	const app = express()

	/**
	 * @todo is "trust proxy" needed?
	 */
	// app.set("trust proxy", true)

	/**
	 * middleware to make req.body json
	 */
	app.use(bodyParser.json())

	/**
	 * Morgan logger
	 * Helpful with development; outputs requests
	 */
	app.use(morgan("dev"))

	/**
	 * Health check endpoints
	 */
	app.get("/status", (req, res) => {
		res.status(200).send("OK").end()
	})

	/**
	 * Load the API routes
	 */
	app.use(config.api.prefix, routes())

	/**
	 * Catch 404 and pass to error handler
	 */
	app.use((req, res, next) => {
		const err = new Error("Not Found")
		err.status = 404

		next(err)
	})

	/**
	 * Error handler
	 */
	app.use((err, req, res, next) => {
		//const err = res.error
		/**
		 * Return specified status code.
		 * @default 500 (Internal Server Error)
		 */
		res.status(err.status || 500)
		res.json({
			errors: {
				message: err.message,
			},
		})
	})

	return app
}
