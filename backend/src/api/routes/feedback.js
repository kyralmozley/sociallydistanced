"use strict"

const { Router } = require("express")
const { celebrate, Joi } = require("celebrate")
const python = require("../../helpers/python")

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

			python("feedback.py", ["true", placeId])
				.then(() => {
					res.status(202).send("Accepted")
				})
				.catch((err) => {
					next(err)
				})
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
				level: Joi.number().integer().required(),
			}),
		}),
		(req, res, next) => {
			const { placeId, suggestion } = req.query

			python("feedback.py", [suggestion.toString(), placeId])
				.then(() => {
					res.status(202).send("Accepted")
				})
				.catch((err) => {
					next(err)
				})
		}
	)
}
