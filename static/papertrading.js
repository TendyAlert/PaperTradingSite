const stocksJson = document.getElementById('user-stocks').textContent.trim();
const stocks = JSON.parse(stocksJson);

const dataJson = document.getElementById('stocks-data').textContent.trim();
const parsedData = JSON.parse(dataJson);

const userBlanceJson = document.getElementById('balance-data').textContent.trim();
const userBalance = JSON.parse(userBlanceJson);

let userBalanceContainer = document.getElementById('user-balance');

let userBalanceHTML = '';

const userId = userBalance[0].user
let currentBalance = parseFloat(userBalance[0].balance)

let userName = ''


const createResetButton = () => {
    resetButton = document.getElementById('reset');
    if (resetButton) {
        resetButton.addEventListener('click', handleReset);
    } else {
        console.error('Reset button not found.');
    }
};

const updateDisplayedBalance = (balance) => {
    floatBalance = parseFloat(balance)
    const fixedBalance = floatBalance.toFixed(2);
    fetch(`/api/user/${userId}/`)
  .then(response => response.json())
  .then(user => {
    userName = user.username
    userBalanceHTML = `
    <h4> Hello ${userName} your balance is $${fixedBalance}</h4>
    <button type='button' id='reset' class='reset' >Reset</button>
    `
    userBalanceContainer.innerHTML = userBalanceHTML
    createResetButton()
  })
  .catch(error => {
    console.error('Error fetching user:', error);
  });
}
updateDisplayedBalance(currentBalance)



let data = {}
let stocks_list = parsedData.map(stock => {
    const fields = stock['fields']
    tickers = Object.keys(fields)
    tickers.forEach(ticker => {
        data[ticker] = JSON.parse(fields[ticker])
    })
})

for(let key in data) {
    data[key] = JSON.parse(data[key])
}

const stocksContainer = document.getElementById('stocks-table-body');

const loadStockPortfolio = () => {
    fetch("/api/stock_portfolio/")
    .then(response => response.json())
    .then(stockPortfolioData => {
        let tableHTML = '';
        stockPortfolioData.forEach(stock => {
            tableHTML += `
            <tr>
                <th class="stocks-table-item user-items">${stock.stock_ticker}</th>
                <td class="stocks-table-item user-items">${stock.quantity}</td>
                <td class="stocks-table-item user-items">${stock.bought_at}</td>
            </tr>
            `;
        });
        stocksContainer.innerHTML = tableHTML;
    })
    .catch(error => {
        console.error("Error loading stock portfolio:", error)
    })
    
}

let currentStock = 'aapl'

handleClick = event => {
    if (event.target.tagName === 'BUTTON' || event.target.parentElement.tagName === 'BUTTON') {
        event.preventDefault();
        id = event.target.id
        currentStock = id
        createChart(currentStock)
    }
}

const buttonContainer = document.getElementById('button-container')
const stockInfo = document.getElementById('stock-info')
let buttonHTML = ''
let infoHTML = ''

const data_keys = Object.keys(data);

data_keys.forEach(key => {
    buttonHTML += `<button type="button" id="${key}">${key.toUpperCase()}</button>`
})

buttonContainer.innerHTML = buttonHTML

buttonContainer.addEventListener('click', handleClick)

let value = 0

const createChart = (name) => {

    separatedData = []

    for(let item in data[name]['Close']){
        tempArr = [parseInt(item), data[name]['Close'][item]]
        separatedData.push(tempArr)
}

    Highcharts.chart('graph-container', {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'Changes from the last quarter of a year',
            align: 'left'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
            align: 'left'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Stock Price'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[6]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[6]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'area',
            name: name,    
            data: separatedData
        }]
    });
    

    const quantity = data[name]['Volume'][separatedData[separatedData.length -1][0]]
    value =  separatedData[separatedData.length -1][1]

    infoHTML = `
        <td class="stock-info-table-item stock-info">${name.toUpperCase()}</td>
        <td class="stock-info-table-item stock-info">${quantity}</td>
        <td class="stock-info-table-item stock-info">${value.toFixed(2)}</td>
    `

    stockInfo.innerHTML = infoHTML;
}

createChart(currentStock)
loadStockPortfolio()

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const updateDatabaseBalance = (newBalance) => {
    fetch(`/api/user_balance/${userId}/`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'balance': newBalance }) 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update balance');
        }
        return response.json();
    })
    .then(data => {
        // Success message or further actions after updating balance
        console.log('User balance updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating user balance:', error);
    });
}

const handleFormSubmit = (event) => {
    event.preventDefault()

    const amountField = form.elements['amount']
    const optionField = form.elements['buy-sell']

    const amount = amountField.value
    const option = optionField.value

    const cost = value * amount

    if (option === 'buy'){
        if(currentBalance < cost){
            alert(`You only have $${currentBalance}, and you are trying to spend , ${cost}`)
            return;}

        currentBalance -= cost;

        const formData = new FormData();
        formData.set('user', userId)
        formData.set('stock_ticker', currentStock.toUpperCase())
        formData.set('cost', value.toFixed(2))
        formData.set('quantity', parseInt(amount))

        fetch("/create_stock_instance/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadStockPortfolio()
            updateDisplayedBalance(currentBalance)
            updateDatabaseBalance(currentBalance)
        })
        .catch(error => {
            console.error("Error creating the stock instance: ", error);
        }
    )
    } else if (option == 'sell'){
        currentBalance += cost
        fetch("/remove_stock_instance/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({'stock_ticker': currentStock, 'amount': amount})
        })
        .then(response => {
            if(!response.ok){
                throw new Error('Failed to remove stock instance')
            }
            return response.json()
        })
        .then(data => {
            if (data && data.hasOwnProperty('success')) {
                // Check if the stock instance was successfully removed
                if (data.success) {
                    // Update the UI and balance
                    loadStockPortfolio();
                    updateDisplayedBalance(currentBalance);
                    updateDatabaseBalance(currentBalance);
                } else {
                    console.error("Stock instance removal failed:", data.message);
                    alert("You do not have enough stocks to sell.")
                }
        
        } else {
            console.error(data.message)
            return
        }
        })
        .catch(error => {
            console.error("Error removing the stock instance: ", error)
        })
    }

    amountField.value = ''
}

form = document.getElementById('stock-info-form')

form.addEventListener('submit', handleFormSubmit)


const handleReset = (event) => {
    event.preventDefault()
    const DEFAULTBALANCE = 10000.00
    updateDisplayedBalance(DEFAULTBALANCE)

    fetch(`/api/user_balance/${userId}/`, {
        method: 'PATCH',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'balance': DEFAULTBALANCE }) 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update balance');
        }
        return response.json();
    })
    .then(data => {
        // Success message or further actions after updating balance
        console.log('User balance updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating user balance:', error);
    });

    fetch(`/delete_all_stocks/${userId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete all stocks')
        }
        return response.json()
    })
    .then(data => {
        console.log('Stocks deleted successfully', data)
        loadStockPortfolio()
    })
    .catch(error => {
        console.error("Error deleting stocks", error)
    })
}
