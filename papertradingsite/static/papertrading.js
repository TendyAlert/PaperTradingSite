const stocksJson = document.getElementById('user-stocks').textContent.trim();
const stocks = JSON.parse(stocksJson);

let tableHTML = '';

const stocksContainer = document.getElementById('stocks-table-body');

stocks.forEach(stock => {
    const fields = stock.fields;
    tableHTML += `
    <tr>
        <th class="stocks-table-item user-items">${fields.stock_ticker}</th>
        <td class="stocks-table-item user-items">${fields.quantity}</td>
        <td class="stocks-table-item user-items">${fields.stock_value}</td>
        <td class="stocks-table-item user-items"><input type='checkbox'></td>
    </tr>
    `;
});

stocksContainer.innerHTML = tableHTML;