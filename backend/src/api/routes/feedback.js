"use strict"

const { Router } = require("express")
const { celebrate, Joi } = require("celebrate")

const route = Router()

/**
 * @todo send feedback to python for training data
 * @todo ratelimiting (block mutliple requests from same IP for same place id)
 */
module.exports = (api) => {
	api.use("/feedback", route)

	/**
	 * Handles positive feedback
	 */
	route.post(
		"/positive",
		celebrate({
			query: Joi.object({
				placeId: Joi.string().required(),
			}),
		}),
		(req, res, next) => {
			const { placeId } = req.query

			// @todo python

			res.status(202).send("Accepted")
		}
	)

	/**
	 * Handles positive feedback
	 */
	route.post(
		"/negative",
		celebrate({
			query: Joi.object({
				placeId: Joi.string().required(),
				suggestion: Joi.number().integer().required()
			}),
		}),
		(req, res, next) => {
			const { placeId, suggestion } = req.query

			// @todo python

			res.status(202).send("Accepted")
		}
	)
}
