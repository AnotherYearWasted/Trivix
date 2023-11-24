const axios = require('axios');

let url = 'https://fapi.binance.com'; // Replace with your API endpoint

// Function to fetch data
/**
 * Get current exchange trading rules and symbol information
 */
async function exchangeInfo(){
    try {
        let URL = url + '/fapi/v1/exchangeInfo'
        let config = {
            method: 'get',
            maxBodyLength: Infinity,
            url: URL,
            headers:{
                'Content-Type': 'application/json',
            },
        }
        //return data to the function
        const response = await axios.request(config).then((response) => {
            return response.data;
        });
        return response;
    }
    catch (error) {
        console.error('Error fetching data:', error.message);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} interval - required, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
 * @param {number} limit - not required, default 500, max 1000
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */


async function klines(symbol, interval, limit = 500, startTime = null, endTime = null){
    try {
        let URL = url + '/fapi/v1/klines'
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
            return response.data;
        });
        return response;
    }
    catch (error) {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {string} interval - required, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
 * @param {number} limit - not required, default 500, max 1000
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function markPriceKlines(symbol, interval, limit = 500, startTime = null, endTime = null){
    try {
        let URL = url + '/fapi/v1/markPriceKlines'
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
            return response.data
        });
        return response
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 * @param {number} limit - not required, default 100, max 1000 
 * @param {number} startTime - not required
 * @param {number} endTime - not required
 */
async function fundingRate(symbol=null, limit=100, startTime=null, endTime=null){
    try {
        let URL = url + '/fapi/v1/fundingRate'
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
            return response.data
        });
        return response
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {*} symbol - not required
 */
async function ticker24h(symbol=null){
    try {
        let URL = url + '/fapi/v1/ticker/24hr'
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
            return response.data
        });
        return response
    }
    catch{
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * 
 * @param {string} symbol - not required 
 */
async function tickerprice(symbol=null){
    try {
        let URL = url + '/fapi/v1/ticker/price'
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
            return response.data
        });
        return response
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {null|string} symbol - not required
 */
async function tickerbookticker(symbol=null){
    try {
        let URL = url + '/fapi/v1/ticker/bookTicker'
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
            return response.data
        });
        return response
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}

/**
 * @param {string} symbol - required
 */
async function openInterest(symbol){
    try {
        let URL = url + '/fapi/v1/openInterest'
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
            return response.data;
        });
        return response;
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
        let URL = url + '/futures/data/openInterestHist'
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
            return response.data
        });
        return response
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
        let URL = url + '/futures/data/topLongShortAccountRatio'
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
            return response.data
        });
        return response
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
        let URL = url + '/futures/data/topLongShortPositionRatio'
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
            return response.data
        });
        return response
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
        let URL = url + '/futures/data/globalLongShortAccountRatio'
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
            return response.data;
        });
        return response;
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
        let URL = url + '/futures/data/takerlongshortRatio'
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
            return response.data
        });
        return response
    }
    catch {
        console.error('Error fetching data:', error.message, error.response.data);
    }
}


console.log('Market function loaded.')
module.exports = {
    exchangeInfo,
    klines,
    markPriceKlines,
    fundingRate,
    ticker24h,
    tickerprice,
    tickerbookticker,
    openInterest,
    openInterestHist,
    topLongShortAccountRatio,
    topLongShortPositionRatio,
    globalLongShortAccountRatio,
    takerlongshortRatio
}