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
});