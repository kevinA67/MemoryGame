// =====================
// Obtener token CSRF
// =====================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// =====================
// Enviar resultado al backend
// =====================
function guardarResultadoPartida(won, score) {
    fetch("/api/save-result/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: `won=${won}&score=${encodeURIComponent(score)}`,
    })
    .then(res => res.json())
    .then(data => console.log("Resultado guardado:", data))
    .catch(err => console.error("Error al guardar:", err));
}

// =====================
// Iniciar juego (tu lógica intacta)
// =====================
function startGame() {
    clearInterval(timer);
    timeLeft = 60;
    score = 0;
    matchedPairs = 0;
    scoreDisplay.textContent = score;
    timeDisplay.textContent = timeLeft;

    let level = parseInt(levelSelect.value);
    totalPairs = level === 1 ? 4 : level === 2 ? 6 : 8;

    let selectedFruits = fruits.slice(0, totalPairs);
    let cards = shuffle([...selectedFruits, ...selectedFruits]);

    gameBoard.innerHTML = '';

    // Calcular columnas para cuadrícula
    const columns = Math.ceil(Math.sqrt(totalPairs * 2));
    gameBoard.style.display = 'grid';
    gameBoard.style.gridTemplateColumns = `repeat(${columns}, 100px)`;
    gameBoard.style.justifyContent = 'center';
    gameBoard.style.gap = '10px';

    cards.forEach(fruit => {
        let card = document.createElement('div');
        card.classList.add('card');
        card.dataset.fruit = fruit;
        card.textContent = '';
        card.style = `
          width: 100px;
          height: 100px;
          font-size: 50px;
          display: flex;
          justify-content: center;
          align-items: center;
          background-color: #4e73df;
          border-radius: 8px;
          cursor: pointer;
          user-select: none;
          color: transparent;
          transition: color 0.3s;
        `;
        card.addEventListener('click', () => flipCard(card));
        gameBoard.appendChild(card);
    });

    timer = setInterval(() => {
        timeLeft--;
        timeDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);
            alert(`Se acabó el tiempo! Puntuación final: ${score}`);
            guardarResultadoPartida(false, score); // Perdida
            gameBoard.innerHTML = '';
        }
    }, 1000);
}

// =====================
// Verificar victoria (llámala desde flipCard cuando sumes matchedPairs)
// =====================
function checkWinCondition() {
    if (matchedPairs === totalPairs) {
        clearInterval(timer);
        alert(`¡Ganaste! Puntuación final: ${score}`);
        guardarResultadoPartida(true, score); // Ganada
    }
}
