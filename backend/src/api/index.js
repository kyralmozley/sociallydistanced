"use strict"

const { Router } = require("express")

const main = require("./routes/main")

module.exports = () => {
	const app = Router()

	/**
	 * Load the routes
	 */
	main(app)

	return app
}
