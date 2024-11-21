let resultadoGuardado = null;  // Variable para almacenar el último resultado

function appendToExpression(value) {
    document.getElementById('expression').value += value;
}

function clearExpression() {
    // Borrar toda la expresión
    document.getElementById('expression').value = '';
    document.getElementById('result').innerText = '';
}

function clearLastDigit() {
    // Borrar el último carácter de la expresión
    const expression = document.getElementById('expression').value;
    document.getElementById('expression').value = expression.slice(0, -1);
}

function calculateTree() {
    let expression = document.getElementById('expression').value;

    // Enviar la expresión al servidor para obtener el árbol y el resultado
    fetch('http://127.0.0.1:5000/tree', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar el resultado
        document.getElementById('tree').innerHTML = data.treeHTML || 'Error al generar el árbol';
        document.getElementById('result').innerText = data.result || 'Error en la expresión';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error al procesar la solicitud';
    });
}

function guardarResultado() {
    const result = document.getElementById('result').innerText;
    if (result && result !== 'Error en la expresión' && result !== 'Error al procesar la solicitud') {
        resultadoGuardado = result;
        alert("Resultado guardado: " + resultadoGuardado);
    } else {
        alert("No hay resultado para guardar.");
    }
}

function insertLastResult() {
    // Verificar si hay un resultado guardado
    if (resultadoGuardado !== null) {
        document.getElementById('expression').value += resultadoGuardado;  // Insertar el último resultado
    } else {
        alert("No hay un resultado guardado.");
    }
}
