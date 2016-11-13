function visitURL(url) {
  chrome.tabs.create({ url: url });
}