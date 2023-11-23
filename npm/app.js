const market = require('./market.js')
const express = require('express')
const app = express()

const port = 2210

app.get('/', async (req, res) => {
    await res.send('Hello World!')
});

app.get('/exchangeInfo', async (req, res) => {
    await market.exchangeInfo().then((result) => {
        res.send(result)
    })
});


app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
});
