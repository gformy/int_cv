class CampaignStorage {
  constructor(items) {
    this.items = items;
    this.hiScoreKey = 'snakecv_hi';
    this.campaignKey = 'snakecv_campaign';
  }

  loadHiScore() {
    return parseInt(localStorage.getItem(this.hiScoreKey) || '0', 10);
  }

  saveHiScore(score) {
    localStorage.setItem(this.hiScoreKey, String(score));
  }

  loadCampaign() {
    const saved = localStorage.getItem(this.campaignKey);

    if (!saved) {
      return {
        collectedItems: [],
        remainingItems: [...this.items],
      };
    }

    const titles = JSON.parse(saved);

    return {
      collectedItems: this.items.filter(item => titles.includes(item.title)),
      remainingItems: this.items.filter(item => !titles.includes(item.title)),
    };
  }

  saveCampaign(collectedItems) {
    const titles = collectedItems.map(item => item.title);
    localStorage.setItem(this.campaignKey, JSON.stringify(titles));
  }

  resetCampaign() {
    localStorage.removeItem(this.campaignKey);
  }
}