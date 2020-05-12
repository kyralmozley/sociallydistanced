const { Router } = require("express")

const route = Router()

module.exports = (api) => {
	api.use("/stats", route)

	/**
	 * Shows the number of searches in the last day, cached data.
	 * @todo actually implement this; it's a dummy api for now
	 */
	route.get("/searches", (req, res) => {
		res.json({
			total: 3,
			timeframe: 86400 * 1000
		})
	})
}