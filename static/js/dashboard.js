document.addEventListener('DOMContentLoaded', function() {
    try {
        const ctx = document.getElementById('lateSignInChart');
        if (!ctx) return;
        
        // Get data from data attributes
        const chartElement = document.getElementById('chart-data');
        if (!chartElement) return;
        
        const chartLabels = JSON.parse(chartElement.dataset.labels || '[]');
        const chartData = JSON.parse(chartElement.dataset.data || '[]');
        
        if (chartLabels.length === 0 || chartData.length === 0) {
            console.warn('No chart data available');
            return;
        }

        new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Late Sign-Ins',
                    data: chartData,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Late Sign-Ins'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing chart:', error);
        const chartContainer = document.getElementById('chart-container');
        if (chartContainer) {
            chartContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error loading chart. Please refresh the page or contact support.
                </div>
            `;
        }
    }
});
