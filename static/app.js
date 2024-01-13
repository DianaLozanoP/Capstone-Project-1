
async function getTransactions() {
    try {
        const response = await fetch('/get-transactions')
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        let amt = []
        let h1 = document.getElementById('prob')
        let labels = Object.keys(data["data"])
        for (let each of labels) {
            amt.push(data["data"][each])
        }
        renderChart(amt, labels)
    } catch (error) {
        console.error(error);
    }
}

function renderChart(amt, labels) {
    let ctx = document.getElementById("myChart").getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Amount',
                data: amt,
                backgroundColor: '#50C878'
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: 'green'
                    }
                }
            }
        }
    });
}

getTransactions();