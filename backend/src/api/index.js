"use strict"

const { Router } = require("express")

const main = require("./routes/main")
const feedback = require("./routes/feedback")

module.exports = () => {
	const app = Router()

	/**
	 * Load the routes
	 */
	main(app)
	feedback(app)

	return app
}
