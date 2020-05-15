"use strict"

const fs = require("fs")
const path = require("path")
const { walk } = require("../util")
const { conf } = require("./configuration")

const cleanCSS = require("clean-css")
const uglifyJS = require("uglify-es")

const staticInput = conf.STATIC_ROOT
const staticOutput = path.join(conf.OUTPUT_ROOT, "static")

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
		} else if (f.endsWith(".gitkeep") || baseName == "README.md") {
			// skip gitkeeps and READMEs
			console.log(`Skipping file \`${f}\``)
			continue
		} else {
			transformed = fs.readFileSync(f, "utf8")
		}

		fs.writeFile(path.join(staticOutput, memberName), transformed, (err) => {
			if (err) {
				console.error(`Could not save \`${f}\`: \`${err}\``)
			} else {
				console.log(`Successfully saved file \`${f}\``)
			}
		})
	}
}
