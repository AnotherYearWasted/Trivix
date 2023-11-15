const axios = require('axios');

let url = 'https://fapi.binance.com/fapi/v1/'; // Replace with your API endpoint

// Function to fetch data
async function exchangeInfo(){
    try {
        let URL = url + 'exchangeInfo'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers:{
                'Content-Type': 'application/json',
            },
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
        });
    }
    catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

async function klines(symbol, interval, limit = 500, startTime = null, endTime = null){
    try {
        let URL = url + 'klines'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                interval: interval,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch (error) {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

async function markPriceKlines(symbol, interval, limit = 500, startTime = null, endTime = null){
    try {
        let URL = url + 'markPriceKlines'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                interval: interval,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

async function fundingRate(symbol=null, limit=100, startTime=null, endTime=null){
    try {
        let URL = url + 'fundingRate'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

async function ticker24h(symbol=null){
    try {
        let URL = url + 'ticker/24hr'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

async function tickerprice(symbol=null){
    try {
        let URL = url + 'ticker/price'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * 
 * @param {null|string} symbol - not required
 */
async function tickerbookticker(symbol=null){
    try {
        let URL = url + 'ticker/bookTicker'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {null|string} symbol - not required
 */
async function openInterest(symbol){
    try {
        let URL = url + 'openInterest'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} period - required, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 30, max 500
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */

async function openInterestHist(symbol, period, limit=30, startTime=null, endTime=null){
    try {
        let URL = url + 'openInterestHist'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                period: period,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} period - required, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 30, max 500
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function topLongShortAccountRatio(symbol, period, limit=30, startTime=null, endTime=null){
    try {
        let URL = url + 'topLongShortAccountRatio'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                period: period,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} period - required, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 30, max 500
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function topLongShortPositionRatio(symbol, period, limit=30, startTime=null, endTime=null){
    try {
        let URL = url + 'topLongShortPositionRatio'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                period: period,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
            console.log("Last updated: " + new Date().toLocaleString());
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} period - required, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 30, max 500
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function globalLongShortAccountRatio(symbol, period, limit=30, startTime=null, endTime=null){
    try {
        let URL = url + 'globalLongShortAccountRatio'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers: {
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                period: period,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} period - required, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 30, max 500
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function takerlongshortRatio(symbol, period, limit=30, startTime=null, endTime=null){
    try {
        let URL = url + 'takerlongshortRatio'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers:{
                'Content-Type': 'application/json',
            },
            params: {
                symbol: symbol,
                period: period,
                limit: limit,
                startTime: startTime,
                endTime: endTime
            }
        }
        const response = await axios.request(config).then((response) => {
            console.log(response.data);
        });
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

console.log('Market function loaded.')