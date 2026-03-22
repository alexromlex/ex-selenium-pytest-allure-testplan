// State
let lastTimestamp = null;
let refreshInterval = null;
let currentRunId = null;
let checkInterval = null;
const all_tests = [];


// Load saved results on startup
document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('collapseContent');
    const icon = document.getElementById('collapseIcon');
    content.style.display = 'none';
    icon.textContent = '▼';
    loadTestsMeatadata();
    loadResults();
});


// Start auto-refresh every 1.5 minutes
function startAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(loadResults, 90000);
}


async function checkForRunningActions() {
    const runBtn = document.getElementById('runBtn');
    try {
        const response = await fetch('https://api.github.com/repos/alexromlex/ex-selenium-pytest-allure-testplan/actions/runs');
        const data = await response.json();
        if(data.workflow_runs){
            const running = data.workflow_runs.some(run => ['queued', 'in_progress'].includes(run.status));
            if(running) {
                showStatus('Tests are currently running...', 'info', 10);
                runBtn.disabled = true;
                runBtn.innerHTML = '<span class="loader"></span> Running...';
                return true;
            } 
        }
        
        runBtn.disabled = false;
        runBtn.innerHTML = 'Run testplan';
        return false;
        
    } catch(error) {
        showStatus('Error: ' + error.message, 'error', 10);
        return false;
    }
}

async function loadResults() {
    try {
        const response = await fetch('../found_tests.json');
        // console.log('Checking for results... ', response);
        if (!response.ok) return;
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error loading results: ', error);
    }
}

async function loadTestsMeatadata() {
    await fetch('../metadata_tests.json')
    .then(response => {
        return response.json();
    })
    .then(data => {
        all_tests.push(...data);
        showStatus('Tests metadata loaded', 'success', 5);
    })
    .catch(error => {
        showStatus('Error loading tests metadata: ' + error.message, 'error', 10);
    });
}

function displayResults(data) {
    const resultsList = document.getElementById('resultsList');
    const resultsCount = document.getElementById('resultsCount');
    const lastQuery = document.getElementById('lastQuery');
    
    // Show query if exists
    if (data.query) {
        lastQuery.innerHTML = `<strong>Last query:</strong> ${JSON.stringify(data.query)}`;
    }
    
    const tests = data.tests || [];
    resultsCount.textContent = tests.length;
    if (tests.length === 0) {
        
        resultsList.innerHTML = '<div class="no-results">No tests found</div>';
        return;
    }
    disableRunButton(true);
    // Build test list
    resultsList.innerHTML = '';
    tests.forEach(test => {
        const testItem = createTestElement(test);
        resultsList.appendChild(testItem);
    });
}

function disableRunButton(enable) {
    const runBtn = document.getElementById('runBtn');
    runBtn.disabled = !enable;
}

function createTestElement(test) {
    const div = document.createElement('div');
    div.className = 'test-item';
    
    // Test ID and name
    const header = document.createElement('div');
    header.className = 'test-header';
    header.innerHTML = `<span class="test-name">[${test.id}] ${test.name}</span>
    `;
    
    // Labels
    const labels = document.createElement('div');
    labels.className = 'test-labels';
    
    if (test.labels) {
        test.labels.forEach(label => {
            Object.entries(label).forEach(([key, value]) => {
                const span = document.createElement('span');
                span.className = `label label-${key}`;
                span.textContent = `${key}: ${value}`;
                labels.appendChild(span);
            });
        });
    }
    
    // Markers
    if (test.markers) {
        test.markers.forEach(marker => {
            const span = document.createElement('span');
            span.className = 'label label-marker';
            span.textContent = marker;
            labels.appendChild(span);
        });
    }
    
    div.appendChild(header);
    div.appendChild(labels);
    
    return div;
}

function isJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}


async function findTests() {
    if (all_tests.length) {
        const filterEngine = new TestFilter(all_tests);
        const filter = document.getElementById('filterInput').value.trim();
        if (!filter) {
            showStatus('Please enter a filter', 'error', 5);
            return;
        }
        if(!isJsonString(filter)) {
            showStatus('Invalid JSON format', 'error', 5);
            return;
        }

        const result1 = filterEngine.filter(JSON.parse(filter));
        // console.log('Filtered tests: ', result1);
        displayResults({tests: result1, query: JSON.parse(filter)});
    } else {
        showStatus('No tests metadata found', 'error', 5);
    }
}

async function runTests() {
    const filter = document.getElementById('filterInput').value.trim();
    const runBtn = document.getElementById('runBtn');
    
    if (!filter) {
        showStatus('Please enter a filter', 'error', 5);
        return;
    }
    if(!isJsonString(filter)) {
        showStatus('Invalid JSON format', 'error', 5);
        return;
    }
    // Check for running workflows before starting a new one
    const isRunning = await checkForRunningActions();
    console.log('Running workflow? ', isRunning);
    if (isRunning) return;

    runBtn.disabled = true;
    runBtn.innerHTML = '<span class="loader"></span> Running...';
    showStatus('Run test started...', 'info', 60);

    await fetch('https://crimson-darkness-b27d.alex-romlex.workers.dev', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filter: JSON.parse(filter)})
    })
    .then(response => {
        if (!response.ok) {
            runBtn.disabled = false;
            runBtn.innerHTML = 'Run testplan';
            showStatus('Failed to start workflow: ' + response.statusText, 'error', 10);
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.status_code !== 200) {
            runBtn.disabled = false;
            runBtn.innerHTML = 'Run testplan';
            showStatus('Failed to start workflow: ' + data.response, 'error', 10);
            return;
        }
        if (data.run_id) {
            currentRunId = data.run_id;
            showStatus(`Workflow (${currentRunId}) started...`, 'info', 140);
            runBtn.disabled = true;
            runBtn.innerHTML = '<span class="loader"></span> Running...';
            refreshInterval = setInterval(() => checkWorkflowStatus(currentRunId), 70000);
        }
    })
    .catch(error => {
        showStatus('Error: ' + error.message, 'error', 10);
    })
}

async function checkWorkflowStatus(runId) {
    const response = await fetch(
        `https://api.github.com/repos/alexromlex/ex-selenium-pytest-allure-testplan/actions/runs/${runId}`,
        {headers: {'Accept': 'application/vnd.github.v3+json'}}
    );
    const runBtn = document.getElementById('runBtn');
    const data = await response.json();
    console.log('[checkWorkflowStatus] data: ', data);
    if(['queued', 'in_progress'].includes(data.status)){
        showStatus(`Tests status ${data.status} ... Next refresh after 1.5 min`, 'info', 90);
        runBtn.disabled = true;
        runBtn.innerHTML = '<span class="loader"></span> Running...';
        
    }
    if (data.status === 'completed') {
        showStatus('Tests completed!', 'success', 5);
        runBtn.disabled = true;
        runBtn.innerHTML = 'Run testplan';
        clearInterval(refreshInterval);
        window.parent.location.href = 'https://alexromlex.github.io/ex-selenium-pytest-allure-testplan/';
    } else {
        showStatus(`Status: ${data.status}`, 'warning', 10);
    }
}

function updateTimestamp(timestamp) {
    const ts = document.getElementById('timestamp');
    if (timestamp) {
        const date = new Date(timestamp);
        ts.textContent = `Last updated: ${date.toLocaleString()}`;
    }
}

function showStatus(message, type, timeout = 5) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status show ${type}`;
    setTimeout(() => status.classList.remove('show'), timeout * 1000)
}

function closeModal() {
    if (window.parent) {
        window.parent.postMessage('close-modal', '*');
    }
}

function toggleCollapse() {
    const content = document.getElementById('collapseContent');
    const icon = document.getElementById('collapseIcon');
    
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        icon.textContent = '▲';
    } else {
        content.style.display = 'none';
        icon.textContent = '▼';
    }
}

class TestFilter {
    constructor(data) {
        this.tests = data || [];
    }

    filter(filters) {
        if (Array.isArray(filters)) {
            const results = [];
            const seenIds = new Set();
            
            for (const singleFilter of filters) {
                const filtered = this._strictFilter(singleFilter);
                for (const test of filtered) {
                    if (!seenIds.has(test.id)) {
                        seenIds.add(test.id);
                        results.push(test);
                    }
                }
            }
            return results;
        }
        
        return this._strictFilter(filters);
    }
    _strictFilter(filters) {
        if (!filters || typeof filters !== 'object') {
            return [];
        }
        
        return this.tests.filter(test => this._matchStrict(test, filters));
    }

    _matchStrict(test, filters) {
        for (const [key, value] of Object.entries(filters)) {
            if (key === 'id') {
                console.log('id')
                if (!this._evaluate(test.id, value)) return false;
                
            } else if (key === 'name') {
                if (!this._evaluate(test.name, value)) return false;
                
            } else if (key === 'markers') {
                if (!this._evaluate(test.markers || [], value)) return false;
                
            } else if (key === 'labels') {
                for (const [labelKey, labelCondition] of Object.entries(value)) {
                    let value = null;
                    for (const label of test.labels || []) {
                        if (label.hasOwnProperty(labelKey)) {
                            value = label[labelKey];
                            break;
                        }
                    }
                    
                    if (!this._evaluate(value, labelCondition)) return false;
                }
            } else {
                // Unknoun param
                return false;
            }
        }
        
        return true;
    }

    _evaluate(value, condition) {
        for (const [op, target] of Object.entries(condition)) {
            switch (op) {
                case 'eq':
                    return value === target;
                    
                case 'neq':
                    return value !== target;
                    
                case 'in':
                    if (value === null || value === undefined) return false;
                    if (Array.isArray(value)) {
                        return value.some(v => target.includes(v));
                    }
                    return target.includes(value);
                    
                case 'nin':
                    if (value === null || value === undefined) return true;
                    if (Array.isArray(value)) {
                        return !value.some(v => target.includes(v));
                    }
                    return !target.includes(value);
                    
                case 'exists':
                    return (value !== null && value !== undefined) === target;
                    
                default:
                    return false;
            }
        }
        return false;
    }

    getUniqueValues(field) {
        const values = new Set();
        
        for (const test of this.tests) {
            if (field === 'epic' || field === 'story' || field === 'severity') {
                for (const label of test.labels || []) {
                    if (label.hasOwnProperty(field)) {
                        values.add(label[field]);
                    }
                }
            } else if (field === 'markers') {
                for (const marker of test.markers || []) {
                    values.add(marker);
                }
            } else {
                values.add(test[field]);
            }
        }
        
        return values;
    }
}
