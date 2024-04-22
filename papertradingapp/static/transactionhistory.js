transactionJson = document.getElementById('transaction-json');
transactionData = JSON.parse(transactionJson.textContent)

let chartData = []
console.log(transactionData)
console.log(transactionData[0].fields.transaction_date)

transactionData.forEach(transaction => {
    const fields = transaction.fields
    const dateString = fields.transaction_date
    const dateObject = new Date(dateString)
    const unixDate = Math.floor(dateObject.getTime() / 1000)
    chartData.push([unixDate, parseFloat(fields.balance)])
});

chartData.sort((a, b) => a[0] - b[0])

console.log(chartData)

Highcharts.chart('chart-container', {
    chart: {
        zoomType: 'x'
    },
    title: {
        text: 'Transaction History',
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
            text: 'Transactions'
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
        name: 'Transaction',    
        data: chartData
    }]
});