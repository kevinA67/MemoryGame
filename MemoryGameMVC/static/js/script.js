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
      gameBoard.innerHTML = '';
    }
  }, 1000);
}
