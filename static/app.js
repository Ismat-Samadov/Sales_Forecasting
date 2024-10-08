async function predictSales() {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;

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

    const data = await response.json();

    // Check if there is a 'message' from the backend, indicating no data found
    if (data.message) {
        document.getElementById('result').innerHTML = `<p>${data.message}</p>`;
        return;
    }

    // Check if the predictions array exists
    if (data.predictions && data.predictions.length > 0) {
        let resultHTML = `<table border="1">
                            <tr>
                                <th>Retailer</th>
                                <th>Product</th>
                                <th>Predicted Sales</th>
                            </tr>`;

        data.predictions.forEach(prediction => {
            resultHTML += `<tr>
                            <td>${prediction.Retailer}</td>
                            <td>${prediction.Product}</td>
                            <td>$${prediction['Predicted Sales'].toFixed(2)}</td>
                           </tr>`;
        });

        resultHTML += '</table>';
        document.getElementById('result').innerHTML = resultHTML;
    } else {
        document.getElementById('result').innerHTML = '<p>No predictions available for the selected date.</p>';
    }
}
