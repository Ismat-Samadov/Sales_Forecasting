document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;
    const shop_id = document.getElementById('shop_id').value;

    const inputData = {
        month: parseInt(month),
        year: parseInt(year),
        shop_id: parseInt(shop_id)
    };

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputData)
    })
    .then(response => response.json())
    .then(data => {
        const chart = document.getElementById('chart');
        chart.src = 'data:image/png;base64,' + data.chart;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
