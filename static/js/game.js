class SnakeCvGame {
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

    this.storage.resetCampaign();
    this.ui.showInfoPlaceholder();
    this.ui.updateScore(this.score, this.hiScore, this.collectedItems.length);
    this.ui.animateSkillBars(this.collectedItems);
  }

  setDirection(direction) {
    if (!this.gameRunning) {
      return;
    }

    const map = {
      UP: { x: 0, y: -1 },
      DOWN: { x: 0, y: 1 },
      LEFT: { x: -1, y: 0 },
      RIGHT: { x: 1, y: 0 },
    };

    const next = map[direction];
    if (!next) {
      return;
    }

    if (next.x === -this.dir.x && next.y === -this.dir.y) {
      return;
    }

    this.nextDir = next;
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