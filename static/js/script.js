function appendToExpression(value) {
    document.getElementById('expression').value += value;
}

function clearExpression() {
    document.getElementById('expression').value = '';
}

function calculateTree() {
    const expression = document.getElementById('expression').value;
    fetch('http://127.0.0.1:5000/tree', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('tree').innerHTML = data.treeHTML;
    });
}
