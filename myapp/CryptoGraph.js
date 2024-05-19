// your_js_file.js
document.addEventListener('DOMContentLoaded', function () {
    function updateGraph() {
        // Fetch cryptocurrency data from your Django view
        fetch('/cryto-rate')  // Use the appropriate URL
            .then(response => response.json())
            .then(data => {
                // Extract Bitcoin and Ethereum prices from the data
                let bitcoinPrice = data.bitcoin_price;
                let ethereumPrice = data.ethereum_price;

                // Create the Matplotlib graph and update as needed
                // ...
            });

        // Schedule the next update
        setTimeout(updateGraph, 5000);  // Update every 5 seconds (adjust as needed)
    }

    // Initial call to update the graph
    updateGraph();
});
