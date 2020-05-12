"use strict";

const config = require("./config")
const loaders = require("./loaders")

/**
 * This is the entry point of the server.
 * We use an async function here because await can't be used in "unscoped" code
 */
async function startServer() {
	const app = await loaders()

	app.listen(config.port, () => {
		console.log(`API listening on port ${config.port}`)
	})
}

startServer()