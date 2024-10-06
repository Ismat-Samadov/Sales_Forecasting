document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const shop_id = document.getElementById('shop_id').value;
    const item_id = document.getElementById('item_id').value;
    const item_price = document.getElementById('item_price').value;
    const item_category_id = document.getElementById('item_category_id').value;
    const item_cnt_month_lag_1 = document.getElementById('item_cnt_month_lag_1').value;
    const item_cnt_month_lag_2 = document.getElementById('item_cnt_month_lag_2').value;
    const item_cnt_month_lag_3 = document.getElementById('item_cnt_month_lag_3').value;

    const inputData = {
        shop_id: parseInt(shop_id),
        item_id: parseInt(item_id),
        item_price: parseFloat(item_price),
        item_category_id: parseInt(item_category_id),
        item_cnt_month_lag_1: parseFloat(item_cnt_month_lag_1),
        item_cnt_month_lag_2: parseFloat(item_cnt_month_lag_2),
        item_cnt_month_lag_3: parseFloat(item_cnt_month_lag_3)
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
        document.getElementById('result').innerHTML = `Predicted Sales: ${data.predicted_sales}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred. Please try again.';
    });
});
