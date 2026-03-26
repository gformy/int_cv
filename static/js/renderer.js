class GameRenderer {
  constructor(canvas, cellSize = 20) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.cellSize = cellSize;
    this.cols = 0;
    this.rows = 0;
    this.foodPulse = 0;
  }

  resize() {
    const wrap = document.getElementById('canvas-wrap');
    const maxW = Math.min(window.innerWidth - 20, 480);
    const maxH = window.innerHeight < 600
      ? window.innerHeight * 0.45
      : Math.min(window.innerHeight - 180, 500);

    this.cols = Math.floor(maxW / this.cellSize);
    this.rows = Math.floor(maxH / this.cellSize);

    this.canvas.width = this.cols * this.cellSize;
    this.canvas.height = this.rows * this.cellSize;
    wrap.style.width = `${this.canvas.width}px`;
  }

  drawIdle() {
    this.ctx.fillStyle = '#050d0a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    this.drawGrid();
  }

  draw(state) {
    this.foodPulse = (this.foodPulse + 0.12) % (Math.PI * 2);

    this.ctx.fillStyle = '#050d0a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.drawGrid();
    this.drawSnake(state.snake, state.dir);
    this.drawFood(state.food);
  }

  drawGrid() {
    this.ctx.strokeStyle = '#0a1f14';
    this.ctx.lineWidth = 0.5;

    for (let x = 0; x <= this.cols; x++) {
      this.ctx.beginPath();
      this.ctx.moveTo(x * this.cellSize, 0);
      this.ctx.lineTo(x * this.cellSize, this.canvas.height);
      this.ctx.stroke();
    }

    for (let y = 0; y <= this.rows; y++) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y * this.cellSize);
      this.ctx.lineTo(this.canvas.width, y * this.cellSize);
      this.ctx.stroke();
    }
  }

  drawSnake(snake, dir) {
    snake.forEach((seg, i) => {
      const isHead = i === 0;
      const t = i / snake.length;

      const gradient = this.ctx.createRadialGradient(
        seg.x * this.cellSize + this.cellSize / 2,
        seg.y * this.cellSize + this.cellSize / 2,
        0,
        seg.x * this.cellSize + this.cellSize / 2,
        seg.y * this.cellSize + this.cellSize / 2,
        this.cellSize * 0.8,
      );

      if (isHead) {
        gradient.addColorStop(0, '#00ffcc');
        gradient.addColorStop(1, '#00cc88');
      } else {
        const g = Math.floor(255 * (1 - t * 0.6));
        gradient.addColorStop(0, `rgba(0,${g},${Math.floor(g * 0.5)},0.95)`);
        gradient.addColorStop(1, `rgba(0,${Math.floor(g * 0.6)},${Math.floor(g * 0.3)},0.8)`);
      }

      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.roundRect(seg.x * this.cellSize + 1, seg.y * this.cellSize + 1, this.cellSize - 2, this.cellSize - 2, isHead ? 6 : 3);
      this.ctx.fill();

      if (isHead) {
        this.drawSnakeHeadDetails(seg, dir);
      }
    });
  }

  drawSnakeHeadDetails(seg, dir) {
    this.ctx.fillStyle = '#000';

    const ex = dir.x === 0 ? [5, 13] : (dir.x > 0 ? [13, 13] : [5, 5]);
    const ey = dir.y === 0 ? [5, 13] : (dir.y > 0 ? [13, 13] : [5, 5]);

    this.ctx.beginPath();
    this.ctx.arc(seg.x * this.cellSize + ex[0], seg.y * this.cellSize + ey[0], 2, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.beginPath();
    this.ctx.arc(seg.x * this.cellSize + ex[1], seg.y * this.cellSize + ey[1], 2, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.fillStyle = '#00ffcc';
    this.ctx.beginPath();
    this.ctx.arc(seg.x * this.cellSize + ex[0], seg.y * this.cellSize + ey[0], 1, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.beginPath();
    this.ctx.arc(seg.x * this.cellSize + ex[1], seg.y * this.cellSize + ey[1], 1, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.shadowColor = '#00ff88';
    this.ctx.shadowBlur = 12;
    this.ctx.fillStyle = 'transparent';
    this.ctx.beginPath();
    this.ctx.roundRect(seg.x * this.cellSize + 1, seg.y * this.cellSize + 1, this.cellSize - 2, this.cellSize - 2, 6);
    this.ctx.fill();
    this.ctx.shadowBlur = 0;
  }

  drawFood(food) {
    if (!food) {
      return;
    }

    const pulse = 1 + Math.sin(this.foodPulse) * 0.15;
    const cx = food.x * this.cellSize + this.cellSize / 2;
    const cy = food.y * this.cellSize + this.cellSize / 2;
    const radius = (this.cellSize / 2 - 2) * pulse;

    this.ctx.shadowColor = food.item.glow;
    this.ctx.shadowBlur = 18;
    this.ctx.fillStyle = food.item.color;
    this.ctx.beginPath();
    this.ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    this.ctx.fill();

    this.ctx.shadowBlur = 0;
    this.ctx.font = `${Math.floor(this.cellSize * 0.65)}px serif`;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(food.item.cat, cx, cy + 1);
  }
}