document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const store_location = document.getElementById('store_location').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            year: year,
            month: month,
            store_location: store_location
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display chart
        const chartDiv = document.getElementById('chart');
        chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="Sales Chart">`;

        // Display sales predictions in a nicely formatted table
        const salesDiv = document.getElementById('sales');
        let salesTable = `<table id="sales-table">
            <thead>
                <tr>
                    <th>Product Category</th>
                    <th>Predicted Sales</th>
                </tr>
            </thead>
            <tbody>`;
        for (let category in data.sales) {
            salesTable += `<tr><td>${category}</td><td>${data.sales[category].toFixed(2)}</td></tr>`;
        }
        salesTable += `</tbody></table>`;
        salesDiv.innerHTML = salesTable;
    })
    .catch(error => console.error('Error:', error));
});
