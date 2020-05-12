const { Router } = require("express")

const stats = require("./routes/stats")

module.exports = () => {
	const app = Router()

	/**
	 * Load the routes
	 */
	stats(app)

	return app
}