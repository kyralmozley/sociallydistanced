"use strict"

const path = require("path")
const dotenv = require("dotenv")

dotenv.config()

process.env.NODE_ENV = process.env.NODE_ENV || "development"

const ROOT = path.join(__dirname, "..", "..")

const conf = {
	ROOT,
	TEMPLATES_ROOT: path.join(ROOT, "templates"),
	SCSS_ROOT: path.join(ROOT, "scss"),
	STATIC_ROOT: path.join(ROOT, "static"),

	OUTPUT_ROOT: path.join(ROOT, "dist"),

	TEMPLATES_EXT: "njk",

	BROWSER_ENV: process.env.ENV || "development",
	NODE_ENV: process.env.NODE_ENV,
	API_BASE_URI: process.env.BASE_URI || "http://localhost:3000/api",
	MAPS_API_KEY: process.env.MAPS_API_KEY,

	HTML_MINIFY_OPTIONS: {
		collapseWhitespace: true,
		collapseInlineTagWhitespace: true,
		keepClosingSlash: true,
		minifyCSS: true,
		minifyJS: true,
		quoteCharacter: '"',
		removeComments: true,
		sortAttributes: true,
		sortClassName: true,
		useShortDoctype: true,
		removeEmptyAttributes: true,
	},
}

module.exports = {
	conf,
}
