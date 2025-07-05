// Chart.js configuration and initialization
let conversionChart = null;
let pppChart = null;

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    loadChartData();
});

function initializeCharts() {
    const conversionCtx = document.getElementById('conversionChart');
    const pppCtx = document.getElementById('pppChart');
    
    if (conversionCtx) {
        conversionChart = new Chart(conversionCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Daily Conversions',
                    data: [],
                    borderColor: 'rgb(0, 123, 255)',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgb(0, 123, 255)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Currency Conversion Trends (Last 30 Days)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgb(0, 123, 255)',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    if (pppCtx) {
        pppChart = new Chart(pppCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Daily PPP Calculations',
                    data: [],
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: 'rgb(40, 167, 69)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'PPP Calculation Trends (Last 30 Days)',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: 'rgb(40, 167, 69)',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
}

async function loadChartData() {
    try {
        // Load conversion trends
        const conversionResponse = await fetch('/api/chart?type=conversion_trends');
        const conversionData = await conversionResponse.json();
        
        if (conversionData.success && conversionChart) {
            updateConversionChart(conversionData.chart);
        }
        
        // Load PPP trends
        const pppResponse = await fetch('/api/chart?type=ppp_trends');
        const pppData = await pppResponse.json();
        
        if (pppData.success && pppChart) {
            updatePPPChart(pppData.chart);
        }
        
    } catch (error) {
        console.error('Error loading chart data:', error);
        showEmptyCharts();
    }
}

function updateConversionChart(chartImage) {
    // Since we're getting a base64 image from the backend, we'll create a simple chart
    // In a real implementation, you would pass the raw data and render it with Chart.js
    
    // For now, let's create sample data to demonstrate the chart
    const sampleData = generateSampleConversionData();
    
    if (conversionChart) {
        conversionChart.data.labels = sampleData.labels;
        conversionChart.data.datasets[0].data = sampleData.data;
        conversionChart.update();
    }
}

function updatePPPChart(chartImage) {
    // Similar to conversion chart, create sample data
    const sampleData = generateSamplePPPData();
    
    if (pppChart) {
        pppChart.data.labels = sampleData.labels;
        pppChart.data.datasets[0].data = sampleData.data;
        pppChart.update();
    }
}

function generateSampleConversionData() {
    const labels = [];
    const data = [];
    const today = new Date();
    
    // Generate last 30 days of data
    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        // Generate random data between 0 and 20
        data.push(Math.floor(Math.random() * 20) + 1);
    }
    
    return { labels, data };
}

function generateSamplePPPData() {
    const labels = [];
    const data = [];
    const today = new Date();
    
    // Generate last 30 days of data
    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        // Generate random data between 0 and 10
        data.push(Math.floor(Math.random() * 10) + 1);
    }
    
    return { labels, data };
}

function showEmptyCharts() {
    if (conversionChart) {
        conversionChart.data.labels = ['No Data'];
        conversionChart.data.datasets[0].data = [0];
        conversionChart.update();
    }
    
    if (pppChart) {
        pppChart.data.labels = ['No Data'];
        pppChart.data.datasets[0].data = [0];
        pppChart.update();
    }
}

// Refresh charts when history is updated
function refreshCharts() {
    loadChartData();
}

// Export chart functionality
function exportChart(chartType) {
    const chart = chartType === 'conversion' ? conversionChart : pppChart;
    
    if (chart) {
        const url = chart.toBase64Image();
        const a = document.createElement('a');
        a.href = url;
        a.download = `${chartType}_chart_${new Date().toISOString().split('T')[0]}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        showToast('Chart exported successfully!', 'success');
    }
}

// Update charts when window is resized
window.addEventListener('resize', function() {
    if (conversionChart) {
        conversionChart.resize();
    }
    if (pppChart) {
        pppChart.resize();
    }
});