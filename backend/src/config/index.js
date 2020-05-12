"use strict";

const dotenv = require("dotenv")

/**
 * This has dotenv load the environment variables into process.env
 */
dotenv.config()

/**
 * Set the NODE_ENV to development by default
 */
process.env.NODE_ENV = process.env.NODE_ENV || "development"

/**
 * Generally acts as a middleman between the application and the
 * environment variables
 */
module.exports = {
	/**
	 * The application is hosted on this port.
	 */
	port: parseInt(process.env.PORT, 10),

	/**
	 * The node environment
	 */
	env: process.env.NODE_ENV,

	/**
	 * api-related configuration options
	 */
	api: {
		/**
		 * The API is served from this route.
		 */
		prefix: "/api",
	},
}