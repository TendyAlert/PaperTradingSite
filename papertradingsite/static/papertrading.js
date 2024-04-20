const stocksJson = document.getElementById('user-stocks').textContent.trim();
const stocks = JSON.parse(stocksJson);

const dataJson = document.getElementById('stocks-data').textContent.trim();
const parsedData = JSON.parse(dataJson);

const userBlanceJson = document.getElementById('balance-data').textContent.trim();
const userBalance = JSON.parse(userBlanceJson);

let userBalanceContainer = document.getElementById('user-balance');

let userBalanceHTML = '';

const userId = userBalance[0].user_id
let startBalance = userBalance[0]['balance']

let userName = ''

const updateDisplayedBalance = (balance) => {
    floatBalance = parseFloat(balance)
    const fixedBalance = floatBalance.toFixed(2);
    fetch(`/api/user/${userId}/`)
  .then(response => response.json())
  .then(user => {
    userName = user.username
    userBalanceHTML = `
    <h4> Hello ${userName} your balance is $${fixedBalance}</h4>
    `
    userBalanceContainer.innerHTML = userBalanceHTML
  })
  .catch(error => {
    console.error('Error fetching user:', error);
  });
}
updateDisplayedBalance(startBalance)



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
    event.preventDefault();
    id = event.target.id
    currentStock = id
    createChart(currentStock)
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

const handleFormSubmit = (event) => {
    event.preventDefault()

    const amountField = form.elements['amount']
    const optionField = form.elements['buy-sell']

    const amount = amountField.value
    const option = optionField.value

    console.log(option)
    const cost = value * amount

    if (option == 'buy'){
        newBalance = startBalance - cost;

        const formData = new FormData();
        formData.set('user_id', userId)
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

            updateDisplayedBalance(newBalance)
        })
        .catch(error => {
            console.error("Error creating the stock instance: ", error);
        }
        )
    }
    
    amountField.value = ''

}

form = document.getElementById('stock-info-form')

form.addEventListener('submit', handleFormSubmit)
