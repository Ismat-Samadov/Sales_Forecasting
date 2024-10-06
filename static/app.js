document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;

    const inputData = {
        month: parseInt(month),
        year: parseInt(year)
    };

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (!data || !data.table || !data.chart) {
            console.error('Invalid server response');
            alert("An error occurred while processing the request. Please try again.");
            return;
        }

        // Display the chart
        if (data.chart) {
            const chart = document.getElementById('chart');
            chart.src = 'data:image/png;base64,' + data.chart;
        }

        // Display the table for the top 5 shops
        if (data.table) {
            const tableBody = document.querySelector('#results-table tbody');
            tableBody.innerHTML = '';  // Clear existing table rows

            data.table.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.shop_id}</td>
                    <td>${row.predicted_sales.toFixed(2)}</td>
                `;
                tableBody.appendChild(tr);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while processing the request. Please check the server and try again.");
    });
});
