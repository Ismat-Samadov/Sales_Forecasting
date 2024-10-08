async function predictSales() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                year: year,
                month: month
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        const resultContainer = document.getElementById('result');

        // Clear previous content and reset opacity
        resultContainer.innerHTML = '';
        resultContainer.classList.remove('show');

        // Check if there is a 'message' from the backend
        if (data.message) {
            resultContainer.innerHTML = `<p>${data.message}</p>`;
            resultContainer.classList.add('show');
            return;
        }

        // Check if predictions exist and generate the table
        if (data.predictions && data.predictions.length > 0) {
            let resultHTML = `<table>
                                <thead>
                                    <tr>
                                        <th>Retailer</th>
                                        <th>Product</th>
                                        <th>Predicted Sales</th>
                                    </tr>
                                </thead>
                                <tbody>`;

            data.predictions.forEach(prediction => {
                resultHTML += `<tr>
                                <td>${prediction.Retailer}</td>
                                <td>${prediction.Product}</td>
                                <td>$${prediction['Predicted Sales'].toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                               </tr>`;
            });

            resultHTML += `</tbody></table>`;
            resultContainer.innerHTML = resultHTML;
            resultContainer.classList.add('show');
        } else {
            resultContainer.innerHTML = '<p>No predictions available for the selected date.</p>';
            resultContainer.classList.add('show');
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        const resultContainer = document.getElementById('result');
        resultContainer.innerHTML = '<p>An error occurred. Please try again later.</p>';
        resultContainer.classList.add('show');
    }
}
