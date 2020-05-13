const { Router } = require("express")
const { celebrate, Joi } = require("celebrate")

const route = Router()

module.exports = (api) => {
	api.use("/main", route)

	/**
	 * Returns data about a place.
	 * This is currently a dummy API while I'm waiting for Kyra to build the ML
	 * Once everything's implemented, we'll need to add daily caching via Redis.
	 */
	route.get(
		"/place",
		celebrate({
			query: Joi.object({
				lat: Joi.number().required(),
				long: Joi.number().required(),
			}),
		}),
		(req, res) => {
			const { lat, long } = req.query
			res.json({
				rating: 0,
				estimated_capacity: 2,

				// return the coordinates back to the client for verification
				coordinates: {
					lat,
					long,
				},
			})
		}
	)

	/**
	 * Shows the number of searches in the last day, cached data.
	 * @todo actually implement this; it's a dummy api for now
	 */
	route.get("/searches", (req, res) => {
		res.json({
			total: 3,
			timeframe: 86400 * 1000,
		})
	})
}
