"use strict"

const path = require("path")
const fs = require("fs")
const rimraf = require("rimraf")
const { conf } = require("./lib/configuration")

const templates = require("./lib/templates")
const content = require("./lib/static")
const style = require("./lib/style")

async function build() {
	// delete (if necessary) and create dist folder
	rimraf.sync(conf.OUTPUT_ROOT)
	fs.mkdirSync(conf.OUTPUT_ROOT)

	// create static directories
	fs.mkdirSync(path.join(conf.OUTPUT_ROOT, "static"))
	fs.mkdirSync(path.join(conf.OUTPUT_ROOT, "static", "css"))
	fs.mkdirSync(path.join(conf.OUTPUT_ROOT, "static", "js"))
	fs.mkdirSync(path.join(conf.OUTPUT_ROOT, "static", "img"))

	// run compilers
	templates()
	await content()
	style()
}

build()
