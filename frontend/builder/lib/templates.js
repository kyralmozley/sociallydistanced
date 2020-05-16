"use strict"

const fs = require("fs")
const path = require("path")
const nunjucks = require("nunjucks")
const { conf } = require("./configuration")

const { minify } = require("html-minifier")

module.exports = () => {
	nunjucks.configure(conf.TEMPLATES_ROOT)

	const dir = fs.readdirSync(conf.TEMPLATES_ROOT)
	dir.forEach((file) => {
		if (path.extname(file) == `.${conf.TEMPLATES_EXT}`) {
			if (path.basename(file).startsWith("_")) {
				console.log(`Skipping file \`${file}\``)
				return false // equivalent to continue in a traditional for loop
			}

			const res = nunjucks.render(file, {
				ENV: conf.BROWSER_ENV,
				BASE_URI: conf.API_BASE_URI,
				MAPS_API_KEY: conf.MAPS_API_KEY,
				CDN_ROOT: conf.CDN_ROOT,
			})

			console.log(`Generated file \`${file}\` successfully`)

			const bareFile = file.replace(/\.[^/.]+$/, "")
			const finalPath = path.join(conf.OUTPUT_ROOT, `${bareFile}.html`)

			// Prepare title comment
			// note: we need the <!doctype html> at the front or IE6 does weird stuff
			const comment = `<!DOCTYPE html>\n<!-- ${bareFile}.html --><!-- File generated: ${new Date().toISOString()} -->\n`

			// Minify the HTML
			let content = minify(res, conf.HTML_MINIFY_OPTIONS)

			// Add the comment
			content = content.replace(/<!doctype html>/i, comment)

			fs.writeFileSync(finalPath, content)

			console.log(`Successfully created \`${finalPath}\``)
		} else {
			console.log(`Skipping file \`${file}\` as it is not a njk file`)
		}
	})
}
