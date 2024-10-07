document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predictionForm');
    const resultSection = document.getElementById('result');
    const chartDiv = document.getElementById('chart');
    const salesTableBody = document.querySelector('#salesTable tbody');

    // Populate shop selection from server
    fetch('/shops')
        .then(response => response.json())
        .then(data => {
            const shopSelect = document.getElementById('shop_id');
            data.shops.forEach(shop => {
                const option = document.createElement('option');
                option.value = shop.shop_id;
                option.textContent = shop.shop_name;
                shopSelect.appendChild(option);
            });
        });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const year = document.getElementById('year').value;
        const shop_id = document.getElementById('shop_id').value;

        // Make POST request to Flask backend
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ year: year, shop_id: shop_id })
        })
        .then(response => response.json())
        .then(data => {
            resultSection.style.display = 'block';

            // Display chart
            chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="Sales Chart" />`;

            // Populate table
            salesTableBody.innerHTML = '';
            data.table.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${row.month}</td><td>${row.predicted_sales}</td>`;
                salesTableBody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
    });
});

document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Get selected shop and year
    const shop = document.getElementById('shop').value;
    const year = document.getElementById('year').value;

    // Send the data to the Flask backend
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            shop_id: parseInt(shop),
            year: parseInt(year)
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display chart
        const chartDiv = document.getElementById('chart');
        chartDiv.innerHTML = `<img src="data:image/png;base64,${data.chart}" alt="Sales Chart">`;

        // Display table
        const tableBody = document.querySelector('#sales-table tbody');
        tableBody.innerHTML = ''; // Clear previous results
        data.table.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${row.month}</td><td>${row.predicted_sales}</td>`;
            tableBody.appendChild(tr);
        });
    })
    .catch(error => console.error('Error:', error));
});
