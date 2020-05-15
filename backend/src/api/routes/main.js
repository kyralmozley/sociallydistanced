"use strict"

const { Router } = require("express")
const { celebrate, Joi } = require("celebrate")
const python = require("../../helpers/python")

const route = Router()

// This is a temporary cache until we implement Redis
let cache = new Map()

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
				placeId: Joi.string().required(),
			}),
		}),
		(req, res, next) => {
			const { placeId } = req.query

			if (cache.has(placeId)) {
				return res.json(cache.get(placeId))
			}
			/**
			 * @todo implement caching with Redis
			 */

			python("main.py", [placeId])
				.then((data) => {
					const result = {
						prediction: data.rating,
						placeId, // echo placeId back to client
						graphPoints: data.day_forecast,
						open: data.open,
					}

					cache.set(placeId, result)
					res.json(result)
				})
				.catch((err) => {
					next(err)
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
