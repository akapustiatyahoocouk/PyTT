class Topic {
  constructor(text, level, href) {
    this.text = text;
    this.level = level;
    this.href = href;
    this.children = [];
  }
}

const rootTopic = new Topic("", 0, "index.html");
const topics = [rootTopic];
console.log(rootTopic);

const toc = new RegExp("^toc([1-9])$");
for (const a of document.getElementsByTagName("a")) {
  const matches = toc.exec(a.className);
  //console.log(matches[1] + ": " + a.innerText + " -> " + a.href);
  a.onclick = function() { 
      window.parent.postMessage({
        "func": "parentFunc",
        "topic": a.href
    }, "*");
    return false;
  };
}
