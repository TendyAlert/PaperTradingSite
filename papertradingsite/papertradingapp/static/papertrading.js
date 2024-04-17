const userBalancesJson = document.getElementById('user-balances').textContent.trim();
const userBalances = JSON.parse(userBalancesJson);

const mapRows = userBalances => {
    console.log('User Data: ', userBalances);

    const userBalancesContainer = document.getElementById('user-balances-container');
    userBalances.forEach(userBalance => {
        const fields = userBalance.fields;
        const userInfo = document.createElement('div');
        userInfo.textContent = `ID: ${userBalance.pk}, First Name: ${fields.first_name}, Last Name: ${fields.last_name}, Balance: ${fields.balance}, Portfolio: ${fields.portfolio}`;
        userBalancesContainer.appendChild(userInfo);
    });
};

mapRows(userBalances);