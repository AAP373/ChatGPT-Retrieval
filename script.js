function runScript() {
    fetch('http://34.173.100.113:5004/run-script', { method: 'POST' })
    .then(response => response.text())
    .then(data => console.log(data));
}

// Assuming you have a button with id 'run-script-button'
document.getElementById('run-script-button').addEventListener('click', runScript);
