const market = require('./market.js')
const express = require('express')
const app = express()

const port = 2210

app.get('/', (req, res) => {
    res.send('Hello World!')
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
});