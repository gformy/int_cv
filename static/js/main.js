window.addEventListener('load', () => {
  const canvas = document.getElementById('c');

  const renderer = new GameRenderer(canvas, 20);
  const ui = new UiManager(CV_ITEMS.length);
  const storage = new CampaignStorage(CV_ITEMS);
  const game = new SnakeCvGame({
    items: CV_ITEMS,
    renderer,
    ui,
    storage,
  });

  const controls = new ControlsManager(
    canvas,
    direction => game.setDirection(direction),
    speed => game.updateSpeed(Number(speed)),
  );

  game.initialize();
  controls.bind();

  window.addEventListener('resize', () => game.handleResize());

  document.getElementById('start-btn').addEventListener('click', () => game.startGame());
  document.getElementById('go-btn').addEventListener('click', () => game.startGame());

  document.getElementById('reset-btn').addEventListener('click', () => {
    game.resetCampaign();
    game.startGame();
  });

  document.getElementById('new-campaign-btn').addEventListener('click', () => {
    game.resetCampaign();
    game.startGame();
  });


  window.addEventListener('load', () => {
  console.log('main.js caricato');

  try {
    const canvas = document.getElementById('c');
    console.log('canvas:', canvas);

    const startBtn = document.getElementById('start-btn');
    const goBtn = document.getElementById('go-btn');
    const resetBtn = document.getElementById('reset-btn');
    const newCampaignBtn = document.getElementById('new-campaign-btn');

    console.log('start-btn:', startBtn);
    console.log('go-btn:', goBtn);
    console.log('reset-btn:', resetBtn);
    console.log('new-campaign-btn:', newCampaignBtn);

    const renderer = new GameRenderer(canvas, 20);
    const ui = new UiManager(CV_ITEMS.length);
    const storage = new CampaignStorage(CV_ITEMS);
    const game = new SnakeCvGame({
      items: CV_ITEMS,
      renderer,
      ui,
      storage,
    });

    const controls = new ControlsManager(
      canvas,
      direction => game.setDirection(direction),
      speed => game.updateSpeed(Number(speed)),
    );

    game.initialize();
    controls.bind();

    window.addEventListener('resize', () => game.handleResize());

    if (startBtn) {
      startBtn.addEventListener('click', () => {
        console.log('click start');
        game.startGame();
      });
    }

    if (goBtn) {
      goBtn.addEventListener('click', () => game.startGame());
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        game.resetCampaign();
        game.startGame();
      });
    }

    if (newCampaignBtn) {
      newCampaignBtn.addEventListener('click', () => {
        game.resetCampaign();
        game.startGame();
      });
    }

    console.log('binding completato');
  } catch (err) {
    console.error('ERRORE main.js:', err);
  }
});
});