const fs = require('fs');
const axios = require('axios');
const market = require('./market.js');
const csv = require('csv-parser');
const exec = require('child_process').exec;

const base_url = 'https://data.binance.vision/data/futures/um/daily/klines/BTCUSDT/'
async function downloadAndUnzip(url, filename) {
    // Remove the dummy file
    if (fs.existsSync(`data/klines/${filename}.dummy`)) {
        await exec(`rm data/klines/${filename}.dummy`, (err, stdout, stderr) => {
            if (err) {
                console.log(err);

                return;
            }
        })
    }
    try {
        const response = await axios({
            method: 'get',
            url: url,
            responseType: 'stream'
        });

        // Write data to file
        let ws = fs.createWriteStream(`data/klines/${filename}.zip`);
        response.data.pipe(ws);

        await new Promise((resolve) => ws.on('finish', resolve));

        console.log(`Zip file ${filename} written`);

        // Unzip file then append the latest csv to BTCUSDT.csv
        await exec(`unzip -p data/klines/${filename}.zip >> data/klines/${filename}.dummy`);
        // Append the dummy file to the csv file, ignore the first line
        await exec(`tail -n +2 data/klines/${filename}.dummy >> data/klines/${filename}.csv`);
        console.log(`CSV file ${filename} written`);
    } catch (error) {
        console.log(error);
        // Retry to unzip
        console.log(`Retrying to unzip ${filename}`);
        await downloadAndUnzip(url, filename);
    }
}

async function get_klines() {
    console.log('Getting data...');
    await market.exchangeInfo().then((result) => {
        result.symbols.forEach(async (symbol) => {
            symbol = symbol.symbol
            if (symbol != 'BTCUSDT') {
                return;
            }
            //for every day from today to previous
            //the url looks like this
            //https://data.binance.vision/data/futures/um/daily/markPriceKlines/BTCUSDT/1m/BTCUSDT-1m-2023-12-12.zip
            
            //check if BTCUSDT.csv exists, if yes then recreate it
            if (fs.existsSync(`data/klines/${symbol}.csv`)) {
                fs.unlinkSync(`data/klines/${symbol}.csv`);
            }
            //create csv file without any data
            for (let i = 10; i >= 1; i--) {
                console.log(i);
    
                let date = new Date();
                date.setDate(date.getDate() - i);
    
                let year = date.getFullYear();
                let month = date.getMonth() + 1;
                let day = date.getDate();
    
                // Format date
                if (month < 10) {
                    month = '0' + month;
                }
    
                if (day < 10) {
                    day = '0' + day;
                }
    
                let url = base_url + '1m/' + symbol + '-1m-' + year + '-' + month + '-' + day + '.zip';
    
                console.log(symbol, url);
    
                // Download and unzip the file
                await downloadAndUnzip(url, symbol);
            }
        });
    });
}
get_klines();
