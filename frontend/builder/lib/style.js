"use strict"

const path = require("path")
const fs = require("fs")
const sass = require("sass")
const { conf } = require("./configuration")

const cleanCSS = require("clean-css")

const scssOutput = path.join(conf.OUTPUT_ROOT, "static", "css", "main.css")

module.exports = () => {
	const scss = sass.renderSync({
		file: path.join(conf.SCSS_ROOT, "main.scss"),
	})

	const input = scss.css
	const comment = `/* ${"main.css"} */ /* File generated: ${new Date().toISOString()} */\n`
	const output = comment + new cleanCSS().minify(input).styles

	fs.writeFileSync(scssOutput, output)

	console.log(`SCSS compiled and outputted to \`${scssOutput}\``)
}
