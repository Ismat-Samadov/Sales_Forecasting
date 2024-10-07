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
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Display chart
            const chartDiv = document.getElementById('chart');
            chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="Sales Chart">`;

            // Display sales table
            const tableBody = document.querySelector('#sales-table tbody');
            tableBody.innerHTML = '';
            for (const [category, sales] of Object.entries(data.sales)) {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${category}</td><td>${sales.toFixed(2)}</td>`;
                tableBody.appendChild(tr);
            }
        }
    })
    .catch(error => console.error('Error:', error));
});
