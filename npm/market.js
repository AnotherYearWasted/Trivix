const axios = require('axios');

let url = 'https://fapi.binance.com/fapi/v1/'; // Replace with your API endpoint

// Function to fetch data
async function exchangeInfo() {
  try {
    let URL = url + 'exchangeInfo'
    let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: URL,
        headers: {
            'Content-Type': 'application/json',
        },
        }
    }
    const response = await axios.get(url);
    console.log('Fetched data:', response.data);
  } catch (error) {
    console.error('Error fetching data:', error.message);
  }
}

// Set up an interval to fetch data every minute (60,000 milliseconds)
const interval = 60 * 1000;
setInterval(fetchData, interval);

// Initial fetch (comment out if you don't want to fetch immediately)
fetchData();
