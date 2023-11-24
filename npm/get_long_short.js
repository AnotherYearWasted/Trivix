const fs = require('fs');
const { get } = require('http');
const market = require('./market.js');
const csv = require('csv-parser');

async function get_long_short_ratio(limit){
    console.log('Getting long/short ratio...');
    await market.exchangeInfo().then((result) => {
        result.symbols.forEach(async (symbol) => {
            try{
                const topLongShortAccountRatioPromise = market.topLongShortAccountRatio(symbol.symbol, '5m', limit=limit);
                const topLongShortPositionRatioPromise = market.topLongShortPositionRatio(symbol.symbol, '5m', limit=limit);
                const globalLongShortAccountRatioPromise = market.globalLongShortAccountRatio(symbol.symbol, '5m', limit=limit);
                const takerLongShortRatioPromise = market.takerlongshortRatio(symbol.symbol, '5m', limit=limit);
                const [topLongShortAccountRatio, topLongShortPositionRatio, globalLongShortAccountRatio, takerLongShortRatio] = await Promise.all([topLongShortAccountRatioPromise, topLongShortPositionRatioPromise, globalLongShortAccountRatioPromise, takerLongShortRatioPromise]);
                const ws = fs.createWriteStream(`data/long_short_ratio/5m/${symbol.symbol}.csv`, { flags: 'a' });
                // If the file is new, then write new column names
                if (fs.statSync(`data/long_short_ratio/5m/${symbol.symbol}.csv`).size == 0){
                    ws.write(`Timestamp,TopRatioAcc,TopLongAcc, TopShortAcc, TopRatioPos, TopLongPos, TopShortPos, GlobalRatioAcc, GlobalLongAcc, GlobalShortAcc, BuySellRatio, BuyVol, SelVol\n`);
                }
                for (i=0; i<topLongShortAccountRatio.length; i++){
                    ws.write(`${topLongShortAccountRatio[i].timestamp},${topLongShortAccountRatio[i].longShortRatio},${topLongShortAccountRatio[i].longAccount},${topLongShortAccountRatio[i].shortAccount},${topLongShortPositionRatio[i].longShortRatio},${topLongShortPositionRatio[i].longAccount},${topLongShortPositionRatio[i].shortAccount},${globalLongShortAccountRatio[i].longShortRatio},${globalLongShortAccountRatio[i].longAccount},${globalLongShortAccountRatio[i].shortAccount},${takerLongShortRatio[0].buySellRatio},${takerLongShortRatio[0].buyVol},${takerLongShortRatio[0].sellVol}\n`);
                }
            }
            catch{
                console.log(`Error getting long/short ratio for ${symbol.symbol}`);
            }
        });
    })
}
get_long_short_ratio(limit=500);
setInterval(get_long_short_ratio.bind(1), 300000);