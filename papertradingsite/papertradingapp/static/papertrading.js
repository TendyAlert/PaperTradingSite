function mapRows(userData) {
    const userBalance = JSON.parse(userData)[0];
    
    console.log('User Data: ', userBalance)
}

fetch('/papertrading/')
    .then(response => response.json())
    .then(mapRows)
    .catch(error => console.error("Error fetching data: ", error));

