"use strict"

/**
 * Copy/paste of 'static.js', but it puts stuff in the project root rather than
 * in 'static'.
 */

const fs = require("fs")
const path = require("path")
const { walk } = require("../util")
const { conf } = require("./configuration")

const cleanCSS = require("clean-css")
const uglifyJS = require("uglify-es")

const writeWalk = require("../vendor/writeFileRecursive")

const staticInput = path.join(conf.ROOT, "root")
const staticOutput = conf.OUTPUT_ROOT

function css(file, name) {
	const input = fs.readFileSync(file, "utf8")
	const comment = `/* ${name} */ /* File generated: ${new Date().toISOString()} */\n`
	const output = comment + new cleanCSS().minify(input)

	return output
}

function js(file, name) {
	const input = fs.readFileSync(file, "utf8")
	const comment = `/* ${name} */ /* File generated: ${new Date().toISOString()} */\n`
	const min = uglifyJS.minify(input, {
		ie8: false,
	})

	if (min.error) {
		return console.error(`Error compiling JS \`${file}\`: \`${min.error}\``)
	}

	const output = comment + min.code
	return output
}

module.exports = async () => {
	for await (const f of walk(staticInput)) {
		const memberName = f.substring(staticInput.length)
		const baseName = path.basename(f)

		// Transform the file
		const ext = path.extname(f, baseName)
		let transformed = ""
		if (ext == ".css") {
			transformed = css(f, baseName)
		} else if (ext == ".js") {
			transformed = js(f, baseName)
		} else if (ext == ".json") {
			transformed = JSON.stringify(JSON.parse(fs.readFileSync(f, "utf8")))
		} else if (f.endsWith(".gitkeep") || baseName == "README.md") {
			// skip gitkeeps and READMEs
			console.log(`Skipping file \`${f}\``)
			continue
		} else {
			transformed = fs.readFileSync(f, "utf8")
		}

		writeWalk(path.join(staticOutput, memberName), transformed, (err) => {
			if (err) {
				console.error(`Could not save \`${f}\`: \`${err}\``)
			} else {
				console.log(`Successfully saved file \`${f}\``)
			}
		})
	}
}
