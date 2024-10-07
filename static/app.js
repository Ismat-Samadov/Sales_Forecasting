document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const year = document.getElementById('year').value;
    const shop_id = document.getElementById('shop').value;

    const data = {
        year: parseInt(year),
        shop_id: parseInt(shop_id)
    };

    // Send the data to the Flask backend
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            // Display the chart
            const chartImg = document.getElementById('sales-chart');
            chartImg.src = 'data:image/png;base64,' + result.chart;
            chartImg.style.display = 'block';

            // Display the table
            const tableContainer = document.getElementById('table-container');
            const tableData = result.table;
            let tableHtml = '<table><tr><th>Month</th><th>Predicted Sales</th></tr>';
            tableData.forEach(row => {
                tableHtml += `<tr><td>${row.month}</td><td>${row.predicted_sales.toFixed(2)}</td></tr>`;
            });
            tableHtml += '</table>';
            tableContainer.innerHTML = tableHtml;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
