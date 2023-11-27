const market = require('./market.js');
const fs = require('fs');
const { get } = require('http');
const csv = require('csv-parser');

//get liquidation orders through wss stream <symbol>@forceOrders
const WebSocket = require('ws');

//get all symbols
market.exchangeInfo().then((result) => {
    let wsstring = 'wss://fstream.binance.com/stream?streams=';
    result.symbols.forEach(async (symbol) => {
        wsstring += `${symbol.symbol.toLowerCase()}@forceOrder/`;
        // Create a new file for each symbol
        fs.writeFile(`data/liquidations/${symbol.symbol}.csv`, '', function (err) {
            if (err) throw err;
        });
    }
    );
    wsstring = wsstring.slice(0, -1);
    const ws = new WebSocket(wsstring);
    ws.on('message', (data) => {
        let json = JSON.parse(data);
        json = json.data.o;
        console.log(json.s, json.S, json.f, json.T, json.q, json.pm, json.ap, json.l, json.z)
        const ws = fs.createWriteStream(`data/liquidations/${json.s}.csv`, { flags: 'a' });
        // If the file is new, then write new column names
        if (fs.statSync(`data/liquidations/${json.s}.csv`).size == 0){
            ws.write(`Symbol,Side,Order Type,Time,Quantity,Price\n`);
        }
        ws.write(`${json.s},${json.S},${json.o},${json.T},${json.q},${json.p}\n`);
    });
})