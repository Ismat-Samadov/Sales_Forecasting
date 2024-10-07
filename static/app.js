document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const shop = document.getElementById('shop').value;
    const monthsToPredict = document.getElementById('months_to_predict').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            shop_id: parseInt(shop),
            months_to_predict: parseInt(monthsToPredict)
        })
    })
    .then(response => response.json())
    .then(data => {
        const chartDiv = document.getElementById('chart');
        chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="Sales Chart">`;

        const tableBody = document.querySelector('#sales-table tbody');
        tableBody.innerHTML = '';
        data.predictions.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${row.month}</td><td>${row.predicted_sales}</td>`;
            tableBody.appendChild(tr);
        });
    })
    .catch(error => console.error('Error:', error));
});
