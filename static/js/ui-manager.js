class UiManager {
  constructor(totalItems) {
    this.totalItems = totalItems;

    this.scoreEl = document.getElementById('score');
    this.hiScoreEl = document.getElementById('hiscore');
    this.collectedEl = document.getElementById('collected');
    this.infoListEl = document.getElementById('info-list');
    this.goScoreEl = document.getElementById('go-score');
    this.goBtnEl = document.getElementById('go-btn');
    this.winMsgEl = document.getElementById('win-msg');
    this.winRecapEl = document.getElementById('win-recap');

    this.startScreen = document.getElementById('start-screen');
    this.gameOverScreen = document.getElementById('gameover-screen');
    this.winScreen = document.getElementById('win-screen');
  }

  updateScore(score, hiScore, collectedCount) {
    this.scoreEl.textContent = score;
    this.hiScoreEl.textContent = hiScore;
    this.collectedEl.textContent = `${collectedCount}/${this.totalItems}`;
  }

  showInfoPlaceholder() {
    this.infoListEl.innerHTML = '<div style="color:var(--dim);font-size:11px;text-align:center;padding:10px;">Mangia i cibi per scoprire il CV!</div>';
  }

  rebuildInfoList(collectedItems) {
    this.infoListEl.innerHTML = '';

    if (collectedItems.length === 0) {
      this.showInfoPlaceholder();
      return;
    }

    [...collectedItems].reverse().forEach(item => {
      const el = document.createElement('div');
      el.className = 'info-item';
      el.innerHTML = `<span class="cat">${item.cat}</span><div class="txt"><strong style="color:${item.color}">${item.title}</strong><br>${item.text}</div>`;
      this.infoListEl.appendChild(el);
    });
  }

  addInfoItem(item) {
    const placeholder = this.infoListEl.querySelector('div[style]');
    if (placeholder) {
      placeholder.remove();
    }

    const el = document.createElement('div');
    el.className = 'info-item';
    el.innerHTML = `<span class="cat">${item.cat}</span><div class="txt"><strong style="color:${item.color}">${item.title}</strong><br>${item.text}</div>`;

    this.infoListEl.insertBefore(el, this.infoListEl.firstChild);
    this.infoListEl.scrollTop = 0;
  }

  animateSkillBars(collectedItems) {
    const categories = collectedItems.map(item => item.cat_name);

    document.querySelectorAll('.skill-fill').forEach(bar => {
      const base = parseInt(bar.dataset.val, 10);
      const skillName = bar.id.replace('sk-', '');
      const boost = categories.filter(cat => (SKILL_MAP[cat] || []).includes(skillName)).length * 3;
      bar.style.width = `${Math.min(100, base + boost)}%`;
    });
  }

  showGameOver(thisRun, done, totalItems, stillLeft) {
    this.goScoreEl.innerHTML =
      `<span style="color:var(--head)">+${thisRun}</span> info questa partita<br>
       Totale: <span style="color:var(--head)">${done}/${totalItems}</span> scoperte<br>
       <span style="color:var(--dim);font-size:10px">${stillLeft > 0 ? `Mancano ancora ${stillLeft} — riprova!` : 'Hai scoperto tutto!'}</span>`;

    this.goBtnEl.textContent = stillLeft > 0 ? '↺ CONTINUA CAMPAGNA' : '🎉 VEDI RIEPILOGO';
    this.gameOverScreen.style.display = 'flex';
  }

  showWin(score, totalItems, collectedItems) {
    this.winMsgEl.innerHTML =
      `Hai scoperto tutte le <strong style="color:var(--head)">${totalItems}</strong> informazioni!<br>
       Punteggio totale: <strong style="color:var(--head)">${score}</strong> pt`;

    this.buildWinRecap(collectedItems);
    this.winScreen.style.display = 'flex';
  }

  buildWinRecap(collectedItems) {
    this.winRecapEl.innerHTML = '';
    const grouped = {};

    collectedItems.forEach(item => {
      if (!grouped[item.cat_name]) {
        grouped[item.cat_name] = {
          cat: item.cat,
          color: item.color,
          items: [],
        };
      }
      grouped[item.cat_name].items.push(item);
    });

    Object.entries(grouped).forEach(([catName, group], gi) => {
      const section = document.createElement('div');
      section.style.cssText = `background:#071410;border:1px solid ${group.color}44;border-radius:8px;overflow:hidden;animation:fadeIn 0.4s ease ${gi * 0.08}s both;`;

      const header = document.createElement('div');
      header.style.cssText = `display:flex;align-items:center;gap:10px;padding:10px 14px;background:${group.color}18;border-bottom:1px solid ${group.color}33;`;
      header.innerHTML = `<span style="font-size:20px">${group.cat}</span>
        <span style="font-family:'Orbitron',monospace;font-size:10px;letter-spacing:2px;color:${group.color}">${catName.toUpperCase()}</span>
        <span style="margin-left:auto;font-size:10px;color:var(--dim)">${group.items.length} info</span>`;
      section.appendChild(header);

      group.items.forEach((item, ii) => {
        const row = document.createElement('div');
        row.style.cssText = `display:flex;gap:12px;padding:10px 14px;border-bottom:1px solid #0a1f14;animation:fadeIn 0.3s ease ${gi * 0.08 + ii * 0.05}s both;`;
        row.innerHTML = `
          <div style="flex:0 0 auto;margin-top:3px;">
            <div style="width:8px;height:8px;border-radius:50%;background:${item.color};box-shadow:0 0 6px ${item.color};margin-top:4px;"></div>
          </div>
          <div>
            <div style="font-family:'Orbitron',monospace;font-size:10px;font-weight:700;color:${item.color};letter-spacing:1px;margin-bottom:3px;">${item.title}</div>
            <div style="font-size:12px;color:#bbb;line-height:1.6;">${item.text}</div>
          </div>`;
        section.appendChild(row);
      });

      this.winRecapEl.appendChild(section);
    });
  }

  hideAllOverlays() {
    [this.startScreen, this.gameOverScreen, this.winScreen].forEach(el => {
      if (el) {
        el.style.display = 'none';
      }
    });
  }
}