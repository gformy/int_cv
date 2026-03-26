class ControlsManager {
  constructor(canvas, onDirectionChange, onSpeedChange) {
    this.canvas = canvas;
    this.onDirectionChange = onDirectionChange;
    this.onSpeedChange = onSpeedChange;
    this.touchStartX = undefined;
    this.touchStartY = undefined;
  }

  bind() {
    this.bindKeyboard();
    this.bindTouch();
    this.bindDpad();
    this.bindSpeed();
  }

  bindKeyboard() {
    document.addEventListener('keydown', event => {
      const map = {
        ArrowUp: 'UP',
        ArrowDown: 'DOWN',
        ArrowLeft: 'LEFT',
        ArrowRight: 'RIGHT',
        KeyW: 'UP',
        KeyS: 'DOWN',
        KeyA: 'LEFT',
        KeyD: 'RIGHT',
      };

      if (!map[event.code]) {
        return;
      }

      event.preventDefault();
      this.onDirectionChange(map[event.code]);
    });
  }

  bindTouch() {
    this.canvas.addEventListener('touchstart', event => {
      this.touchStartX = event.touches[0].clientX;
      this.touchStartY = event.touches[0].clientY;
      event.preventDefault();
    }, { passive: false });

    this.canvas.addEventListener('touchend', event => {
      if (this.touchStartX === undefined) {
        return;
      }

      const dx = event.changedTouches[0].clientX - this.touchStartX;
      const dy = event.changedTouches[0].clientY - this.touchStartY;

      if (Math.abs(dx) > Math.abs(dy)) {
        this.onDirectionChange(dx > 0 ? 'RIGHT' : 'LEFT');
      } else {
        this.onDirectionChange(dy > 0 ? 'DOWN' : 'UP');
      }

      event.preventDefault();
    }, { passive: false });
  }

  bindDpad() {
    const bindings = {
      'dpad-up': 'UP',
      'dpad-down': 'DOWN',
      'dpad-left': 'LEFT',
      'dpad-right': 'RIGHT',
    };

    Object.entries(bindings).forEach(([id, direction]) => {
      const element = document.getElementById(id);
      if (!element) {
        return;
      }

      element.addEventListener('touchstart', () => this.onDirectionChange(direction));
      element.addEventListener('click', () => this.onDirectionChange(direction));
    });
  }

  bindSpeed() {
    const slider = document.getElementById('speed-slider');
    if (!slider) {
      return;
    }

    slider.addEventListener('input', event => {
      this.onSpeedChange(event.target.value);
    });
  }
}