"use strict"

/**
 * This is not designed for production
 */

const path = require("path")
const express = require("express")
const sass = require("sass")
const morgan = require("morgan")
const nunjucks = require("express-nunjucks")
const { config } = require("dotenv")

config()
const app = express()

const env = process.env.NODE_ENV || "development"
const isDev = env == "development"
const port = process.env.PORT || 8080

const base = path.join(__dirname, "..")
const assets = path.join(base, "static")

/**
 * Morgan logger
 * Logs HTTP requests, used for development
 */
app.use(morgan("dev"))

/**
 * Setup nunjucks
 * (HTML templating)
 */
app.set("views", path.join(__dirname, "..", "templates"))
app.set("view engine", "njk")
nunjucks(app, {
	watch: isDev,
	noCache: isDev,
	globals: {
		ENV: process.env.ENV,
		BASE_URI: process.env.BASE_URI,
		MAPS_API_KEY: process.env.MAPS_API_KEY,
	},
})

/**
 * SCSS
 */
const scss = sass.renderSync({ file: path.join(base, "scss", "main.scss") })
app.use("/static/css/main.css", (req, res) => {
	res.setHeader("Content-Type", "text/css")
	res.send(scss.css)
})

/**
 * Static directories
 * This means you can do /html, /img, etc.
 */
app.use("/static", express.static(assets))

/**
 * Routes
 */
app.get("/", (req, res) => {
	res.render("index")
})

/**
 * 404 handler
 */
app.use((req, res) => {
	res.render("404")
})

/**
 * Listen for requests
 */
app.listen(port, () => {
	console.log(`dev-server listening on port ${port}.`)
})
