document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(document.getElementById('prediction-form'));
    const resultDiv = document.getElementById('result');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.textContent = data.prediction;
            resultDiv.className = 'result success';
        } else {
            resultDiv.textContent = 'Error: ' + data.error;
            resultDiv.className = 'result error';
        }
    } catch (error) {
        resultDiv.textContent = 'Error: Unable to connect to the server.';
        resultDiv.className = 'result error';
    }
});