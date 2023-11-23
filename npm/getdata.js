const fs = require('fs');
const { get } = require('http');
const market = require('./market.js');
const csv = require('csv-parser');

async function get_klines_and_open_interest_and_long_short_ratio() {
    console.log('Getting data...');
    await market.exchangeInfo().then((result) => {
        result.symbols.forEach(async (symbol) => {
            const klinesPromise = market.klines(symbol.symbol, '1m', limit=2);
            const openInterestPromise = market.openInterest(symbol.symbol);
            const [klines, openInterest] = await Promise.all([klinesPromise, openInterestPromise]);

            const ws = fs.createWriteStream(`data/candles/1m/${symbol.symbol}.csv`, { flags: 'a' });

            // If the file is new, then write new column names
            if (fs.statSync(`data/candles/1m/${symbol.symbol}.csv`).size == 0){
                ws.write(`Open Time,Open,High,Low,Close,Volume,Close Time,Quote Asset Volume,Number of Trades,Taker buy base asset volume,Taker buy quote asset volume,Ignore,Open Interest\n`);
            }
            // Write all except the last kline
            for (i=0; i<klines.length-1; i++){
                ws.write(`${klines[i][0]},${klines[i][1]},${klines[i][2]},${klines[i][3]},${klines[i][4]},${klines[i][5]},${klines[i][6]},${klines[i][7]},${klines[i][8]},${klines[i][9]},${klines[i][10]},${klines[i][11]},${openInterest.openInterest}\n`);
            }
            ws.end();
        });
    });
}

setInterval(get_klines_and_open_interest_and_long_short_ratio, 60000);