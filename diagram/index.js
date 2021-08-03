const { json } = require('body-parser')
const { buildDiagramSVG } = require('./diagram-builder.js')
const express = require('express')

const app = express()
const port = 3000

app.get('/diagram', (req, res) => {
  let svg = buildDiagramSVG() // req.body
  res.json({diagram: svg});
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})