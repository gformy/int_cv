class SnakeCvGame {
  constructor({ items, renderer, ui, storage }) {
    this.items = items;
    this.renderer = renderer;
    this.ui = ui;
    this.storage = storage;

    this.totalItems = items.length;
    this.speedMs = 150;
    this.gameInterval = null;

    this.snake = [];
    this.dir = { x: 1, y: 0 };
    this.nextDir = { x: 1, y: 0 };

    // 🔥 nuova gestione input
    this.directionQueue = [];
    this.pendingReverse = null;

    this.food = null;
    this.score = 0;
    this.gameRunning = false;

    this.collectedItems = [];
    this.remainingItems = [];
    this.sessionItems = [];
    this.hiScore = 0;
  }

  initialize() {
    this.hiScore = this.storage.loadHiScore();

    const campaign = this.storage.loadCampaign();
    this.collectedItems = campaign.collectedItems;
    this.remainingItems = campaign.remainingItems;

    this.ui.rebuildInfoList(this.collectedItems);
    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.ui.animateSkillBars(this.collectedItems);

    this.renderer.resize();
    this.renderer.drawIdle();
  }

  handleResize() {
    this.renderer.resize();
    if (!this.gameRunning) {
      this.renderer.drawIdle();
    }
  }

  startGame() {
    this.ui.hideAllOverlays();
    this.renderer.resize();

    if (this.remainingItems.length === 0) {
      this.resetCampaign();
    }

    this.snake = [
      { x: Math.floor(this.renderer.cols / 2), y: Math.floor(this.renderer.rows / 2) },
      { x: Math.floor(this.renderer.cols / 2) - 1, y: Math.floor(this.renderer.rows / 2) },
      { x: Math.floor(this.renderer.cols / 2) - 2, y: Math.floor(this.renderer.rows / 2) },
    ];

    this.dir = { x: 1, y: 0 };
    this.nextDir = { x: 1, y: 0 };

    this.directionQueue = [];
    this.pendingReverse = null;

    this.score = 0;
    this.sessionItems = [];
    this.gameRunning = true;

    this.remainingItems = this.shuffle([...this.remainingItems]);

    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.spawnFood();

    clearInterval(this.gameInterval);
    this.gameInterval = setInterval(() => this.tick(), this.speedMs);
  }

  tick() {
    if (!this.gameRunning) return;

    this.resolveDirectionForCurrentTick();

    this.dir = { ...this.nextDir };

    const head = {
      x: this.snake[0].x + this.dir.x,
      y: this.snake[0].y + this.dir.y,
    };

    if (this.isWallCollision(head) || this.isSelfCollision(head)) {
      this.endGame();
      return;
    }

    this.snake.unshift(head);

    if (this.food && head.x === this.food.x && head.y === this.food.y) {
      this.eatFood();
    } else {
      this.snake.pop();
    }

    this.renderer.draw({
      snake: this.snake,
      dir: this.dir,
      food: this.food,
    });
  }

  // 🔥 cuore del sistema input
  resolveDirectionForCurrentTick() {
    const reference = this.nextDir;

    // 1. prova a trovare una direzione valida nella coda
    const index = this.directionQueue.findIndex(d =>
      this.isLegalTurn(d, reference)
    );

    if (index !== -1) {
      const [dir] = this.directionQueue.splice(index, 1);
      this.nextDir = dir;
      this.pendingReverse = null;
      return;
    }

    // 2. prova il reverse se diventa legale
    if (this.pendingReverse && this.isLegalTurn(this.pendingReverse, reference)) {
      this.nextDir = this.pendingReverse;
      this.pendingReverse = null;
    }
  }

  setDirection(direction) {
    if (!this.gameRunning) return;

    const map = {
      UP: { x: 0, y: -1 },
      DOWN: { x: 0, y: 1 },
      LEFT: { x: -1, y: 0 },
      RIGHT: { x: 1, y: 0 },
    };

    const input = map[direction];
    if (!input) return;

    const last =
      this.directionQueue.length > 0
        ? this.directionQueue[this.directionQueue.length - 1]
        : this.nextDir;

    // ignora duplicati inutili
    if (this.isSameDirection(input, last)) return;

    // reverse → NON blocca la coda
    if (this.isOppositeDirection(input, last)) {
      this.pendingReverse = input;
      return;
    }

    // coda limitata
    if (this.directionQueue.length < 3) {
      this.directionQueue.push(input);
    }
  }

  isLegalTurn(candidate, reference) {
    return !this.isSameDirection(candidate, reference) &&
           !this.isOppositeDirection(candidate, reference);
  }

  isOppositeDirection(a, b) {
    return a.x === -b.x && a.y === -b.y;
  }

  isSameDirection(a, b) {
    return a.x === b.x && a.y === b.y;
  }

  isWallCollision(head) {
    return (
      head.x < 0 ||
      head.x >= this.renderer.cols ||
      head.y < 0 ||
      head.y >= this.renderer.rows
    );
  }

  isSelfCollision(head) {
    return this.snake.some(s => s.x === head.x && s.y === head.y);
  }

  eatFood() {
    const item = this.food.item;

    this.score += 10;
    this.sessionItems.push(item);
    this.collectedItems.push(item);

    this.storage.saveCampaign(this.collectedItems);

    if (this.score > this.hiScore) {
      this.hiScore = this.score;
      this.storage.saveHiScore(this.hiScore);
    }

    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.ui.addInfoItem(item);
    this.ui.animateSkillBars(this.collectedItems);

    if (this.remainingItems.length === 0) {
      setTimeout(() => this.winGame(), 200);
    } else {
      this.spawnFood();
    }
  }

  spawnFood() {
    let pos;
    const item = this.remainingItems.pop();

    do {
      pos = {
        x: Math.floor(Math.random() * this.renderer.cols),
        y: Math.floor(Math.random() * this.renderer.rows),
      };
    } while (this.snake.some(s => s.x === pos.x && s.y === pos.y));

    this.food = { ...pos, item };
  }

  endGame() {
    this.gameRunning = false;
    clearInterval(this.gameInterval);

    const stillLeft = this.remainingItems.length + (this.food ? 1 : 0);
    const thisRun = this.sessionItems.length;
    const done = this.collectedItems.length;

    if (this.score > this.hiScore) {
      this.hiScore = this.score;
      this.storage.saveHiScore(this.hiScore);
    }

    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.ui.showGameOver(thisRun, done, this.totalItems, stillLeft);
  }

  winGame() {
    this.gameRunning = false;
    clearInterval(this.gameInterval);
    this.ui.showWin(this.score, this.totalItems, this.collectedItems);
  }

  resetCampaign() {
    this.collectedItems = [];
    this.remainingItems = [...this.items];
    this.sessionItems = [];
    this.food = null;

    this.directionQueue = [];
    this.pendingReverse = null;

    this.storage.resetCampaign();
    this.ui.showInfoPlaceholder();
    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.ui.animateSkillBars(this.collectedItems);
  }

  updateSpeed(value) {
    const speeds = [220, 175, 140, 110, 80];
    this.speedMs = speeds[value - 1];

    if (this.gameRunning) {
      clearInterval(this.gameInterval);
      this.gameInterval = setInterval(() => this.tick(), this.speedMs);
    }
  }

  shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
}