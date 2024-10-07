document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('prediction-form');
    const shopDropdown = document.getElementById('shop');
    const yearDropdown = document.getElementById('year');

    if (form && shopDropdown && yearDropdown) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get selected shop and year
            const shop = shopDropdown.value;
            const year = yearDropdown.value;

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
    }
});
