const expressLoader = require("./express")

/**
 * This calls all the other loaders in the required order.
 * @returns {ExpressApp} App
 */
module.exports = async () => {
	const app = await expressLoader()

	return app
}