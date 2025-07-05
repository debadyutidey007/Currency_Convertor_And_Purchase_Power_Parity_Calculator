// Global variables
let currencyData = {};
let countryData = {};

// DOM elements
const converterForm = document.getElementById('converterForm');
const pppForm = document.getElementById('pppForm');
const fromCurrency = document.getElementById('fromCurrency');
const toCurrency = document.getElementById('toCurrency');
const amount = document.getElementById('amount');
const result = document.getElementById('result');
const fromSymbol = document.getElementById('fromSymbol');
const toSymbol = document.getElementById('toSymbol');
const swapBtn = document.getElementById('swapCurrencies');
const conversionInfo = document.getElementById('conversionInfo');
const exchangeRate = document.getElementById('exchangeRate');
const lastUpdatedTime = document.getElementById('lastUpdatedTime');

const fromCountry = document.getElementById('fromCountry');
const toCountry = document.getElementById('toCountry');
const income = document.getElementById('income');
const equivalentIncome = document.getElementById('equivalentIncome');
const pppResults = document.getElementById('pppResults');
const pppRate = document.getElementById('pppRate');
const bigMacIndex = document.getElementById('bigMacIndex');
const costOfLiving = document.getElementById('costOfLiving');

const loadingSpinner = document.getElementById('loadingSpinner');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadCurrencyData();
    loadCountryData();
    loadHistories();
    setupEventListeners();
});

function initializeApp() {
    console.log('Currency Converter Pro initialized');
    
    // Update currency symbols on page load
    updateCurrencySymbols();
    
    // Initialize Bootstrap components
    const toastBootstrap = new bootstrap.Toast(toast);
}

function setupEventListeners() {
    // Converter form
    if (converterForm) {
        converterForm.addEventListener('submit', handleCurrencyConversion);
    }
    
    // PPP form
    if (pppForm) {
        pppForm.addEventListener('submit', handlePPPCalculation);
    }
    
    // Currency change events
    if (fromCurrency) {
        fromCurrency.addEventListener('change', updateCurrencySymbols);
    }
    if (toCurrency) {
        toCurrency.addEventListener('change', updateCurrencySymbols);
    }
    
    // Swap currencies button
    if (swapBtn) {
        swapBtn.addEventListener('click', swapCurrencies);
    }
    
    // History tabs
    const historyTabs = document.querySelectorAll('#historyTabs button');
    historyTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const target = event.target.getAttribute('data-bs-target');
            if (target === '#conversion-history') {
                loadConversionHistory();
            } else if (target === '#ppp-history') {
                loadPPPHistory();
            }
        });
    });
    
    // Export buttons
    const exportConversions = document.getElementById('exportConversions');
    const exportPPP = document.getElementById('exportPPP');
    
    if (exportConversions) {
        exportConversions.addEventListener('click', () => exportData('conversion'));
    }
    if (exportPPP) {
        exportPPP.addEventListener('click', () => exportData('ppp'));
    }
    
    // Delete buttons
    const deleteConversions = document.getElementById('deleteConversions');
    const deletePPP = document.getElementById('deletePPP');
    
    if (deleteConversions) {
        deleteConversions.addEventListener('click', () => deleteHistory('conversion'));
    }
    if (deletePPP) {
        deletePPP.addEventListener('click', () => deleteHistory('ppp'));
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Currency conversion functionality
async function handleCurrencyConversion(e) {
    e.preventDefault();
    
    const fromCurr = fromCurrency.value;
    const toCurr = toCurrency.value;
    const amountVal = parseFloat(amount.value);
    
    if (!fromCurr || !toCurr || !amountVal) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    if (fromCurr === toCurr) {
        result.value = amountVal.toFixed(4);
        showConversionInfo(1.0);
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from_currency: fromCurr,
                to_currency: toCurr,
                amount: amountVal
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            result.value = data.result.toFixed(4);
            showConversionInfo(data.exchange_rate);
            showToast('Conversion successful!', 'success');
            
            // Refresh history
            loadConversionHistory();
        } else {
            showToast(data.error || 'Conversion failed', 'error');
        }
    } catch (error) {
        console.error('Conversion error:', error);
        showToast('Network error. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// PPP calculation functionality
async function handlePPPCalculation(e) {
    e.preventDefault();
    
    const fromCountryVal = fromCountry.value;
    const toCountryVal = toCountry.value;
    const incomeVal = parseFloat(income.value);
    
    if (!fromCountryVal || !toCountryVal || !incomeVal) {
        showToast('Please fill in all fields', 'error');
        return;
    }
    
    if (fromCountryVal === toCountryVal) {
        equivalentIncome.value = incomeVal.toFixed(2);
        showPPPResults(1.0, 1.0, 1.0);
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/ppp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from_country: fromCountryVal,
                to_country: toCountryVal,
                income: incomeVal
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            equivalentIncome.value = data.equivalent_income.toFixed(2);
            showPPPResults(data.ppp_rate, data.big_mac_index, data.cost_of_living_index);
            showToast('PPP calculation successful!', 'success');
            
            // Refresh history
            loadPPPHistory();
        } else {
            showToast(data.error || 'PPP calculation failed', 'error');
        }
    } catch (error) {
        console.error('PPP calculation error:', error);
        showToast('Network error. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Helper functions
function updateCurrencySymbols() {
    const fromCurr = fromCurrency.value;
    const toCurr = toCurrency.value;
    
    // Update symbols based on currency selection
    const currencySymbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CAD': '$', 'AUD': '$',
        'CHF': 'CHF', 'CNY': '¥', 'INR': '₹', 'BRL': 'R$', 'RUB': '₽',
        'KRW': '₩', 'MXN': '$', 'SGD': '$', 'HKD': '$', 'NOK': 'kr',
        'SEK': 'kr', 'DKK': 'kr', 'PLN': 'zł', 'CZK': 'Kč', 'HUF': 'Ft',
        'ILS': '₪', 'ZAR': 'R', 'TRY': '₺', 'THB': '฿', 'MYR': 'RM',
        'PHP': '₱', 'IDR': 'Rp', 'VND': '₫'
    };
    
    fromSymbol.textContent = currencySymbols[fromCurr] || '$';
    toSymbol.textContent = currencySymbols[toCurr] || '$';
}

function swapCurrencies() {
    const fromVal = fromCurrency.value;
    const toVal = toCurrency.value;
    
    fromCurrency.value = toVal;
    toCurrency.value = fromVal;
    
    updateCurrencySymbols();
    
    // Clear results
    result.value = '';
    conversionInfo.style.display = 'none';
}

function showConversionInfo(rate) {
    exchangeRate.textContent = `1 ${fromCurrency.value} = ${rate.toFixed(6)} ${toCurrency.value}`;
    lastUpdatedTime.textContent = new Date().toLocaleString();
    conversionInfo.style.display = 'block';
}

function showPPPResults(pppRateVal, bigMacVal, costOfLivingVal) {
    pppRate.textContent = pppRateVal.toFixed(4);
    bigMacIndex.textContent = bigMacVal.toFixed(4);
    costOfLiving.textContent = costOfLivingVal.toFixed(4);
    pppResults.style.display = 'block';
}

function showLoading(show) {
    if (show) {
        loadingSpinner.classList.add('show');
    } else {
        loadingSpinner.classList.remove('show');
    }
}

function showToast(message, type = 'info') {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
    const toastHeader = toast.querySelector('.toast-header');
    
    // Update toast style based on type
    toast.className = 'toast';
    toastHeader.className = 'toast-header';
    
    switch (type) {
        case 'success':
            toast.classList.add('bg-success', 'text-white');
            toastHeader.classList.add('bg-success', 'text-white');
            break;
        case 'error':
            toast.classList.add('bg-danger', 'text-white');
            toastHeader.classList.add('bg-danger', 'text-white');
            break;
        case 'warning':
            toast.classList.add('bg-warning', 'text-dark');
            toastHeader.classList.add('bg-warning', 'text-dark');
            break;
        default:
            toast.classList.add('bg-info', 'text-white');
            toastHeader.classList.add('bg-info', 'text-white');
    }
    
    toastMessage.textContent = message;
    toastBootstrap.show();
}

// Data loading functions
async function loadCurrencyData() {
    try {
        const response = await fetch('/api/currencies');
        const data = await response.json();
        
        if (data.success) {
            currencyData = data.currencies;
        }
    } catch (error) {
        console.error('Error loading currency data:', error);
    }
}

async function loadCountryData() {
    try {
        const response = await fetch('/api/countries');
        const data = await response.json();
        
        if (data.success) {
            countryData = data.countries;
        }
    } catch (error) {
        console.error('Error loading country data:', error);
    }
}

async function loadHistories() {
    loadConversionHistory();
    loadPPPHistory();
}

async function loadConversionHistory() {
    try {
        const response = await fetch('/api/history?type=conversion&limit=20');
        const data = await response.json();
        
        if (data.success) {
            displayConversionHistory(data.history);
        }
    } catch (error) {
        console.error('Error loading conversion history:', error);
        displayConversionHistory([]);
    }
}

async function loadPPPHistory() {
    try {
        const response = await fetch('/api/history?type=ppp&limit=20');
        const data = await response.json();
        
        if (data.success) {
            displayPPPHistory(data.history);
        }
    } catch (error) {
        console.error('Error loading PPP history:', error);
        displayPPPHistory([]);
    }
}

function displayConversionHistory(history) {
    const tbody = document.getElementById('conversionHistoryBody');
    
    if (history.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-info-circle me-2"></i>
                    No conversion history available
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = history.map(item => `
        <tr>
            <td>${new Date(item.conversion_time).toLocaleString()}</td>
            <td>
                <strong>${item.from_currency}</strong>
                <br>
                <small class="text-muted">${item.from_currency_name || ''}</small>
            </td>
            <td>
                <strong>${item.to_currency}</strong>
                <br>
                <small class="text-muted">${item.to_currency_name || ''}</small>
            </td>
            <td>${parseFloat(item.amount).toFixed(4)}</td>
            <td>${parseFloat(item.result).toFixed(4)}</td>
            <td>${parseFloat(item.exchange_rate).toFixed(6)}</td>
        </tr>
    `).join('');
}

function displayPPPHistory(history) {
    const tbody = document.getElementById('pppHistoryBody');
    
    if (history.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-info-circle me-2"></i>
                    No PPP history available
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = history.map(item => `
        <tr>
            <td>${new Date(item.calculation_time).toLocaleString()}</td>
            <td>
                <strong>${item.from_country}</strong>
                <br>
                <small class="text-muted">${item.from_country_name || ''}</small>
            </td>
            <td>
                <strong>${item.to_country}</strong>
                <br>
                <small class="text-muted">${item.to_country_name || ''}</small>
            </td>
            <td>$${parseFloat(item.income_from).toFixed(2)}</td>
            <td>$${parseFloat(item.income_equivalent).toFixed(2)}</td>
            <td>${parseFloat(item.ppp_rate).toFixed(4)}</td>
        </tr>
    `).join('');
}

// Export functionality
async function exportData(type) {
    try {
        showLoading(true);
        
        const response = await fetch(`/api/export?type=${type}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${type}_history_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast('Data exported successfully!', 'success');
        } else {
            showToast('Export failed. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Export error:', error);
        showToast('Export failed. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Update last updated time
function updateLastUpdated() {
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {
        lastUpdatedElement.textContent = new Date().toLocaleString();
    }
}

// Set interval to update last updated time
setInterval(updateLastUpdated, 60000); // Update every minute

// Delete history functionality
async function deleteHistory(type) {
    // Show confirmation dialog
    const historyType = type === 'conversion' ? 'Conversion' : 'PPP';
    const confirmed = confirm(`Are you sure you want to delete all ${historyType} history? This action cannot be undone.`);
    
    if (!confirmed) {
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/delete-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type: type })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast(`${historyType} history deleted successfully!`, 'success');
            
            // Reload the appropriate history
            if (type === 'conversion') {
                loadConversionHistory();
            } else {
                loadPPPHistory();
            }
            
            // Refresh charts as well
            if (typeof refreshCharts === 'function') {
                refreshCharts();
            }
        } else {
            throw new Error(data.error || 'Failed to delete history');
        }
    } catch (error) {
        console.error('Delete history error:', error);
        showToast('Failed to delete history. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}