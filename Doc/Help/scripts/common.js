function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function resize_iframes() {
  let ih = window.innerHeight;
  //console.log(ih);
  document.querySelector('#navigatorframe').height = ih - 164;
  document.querySelector('#contentframe').height = ih - 164;
}

window.addEventListener("resize", (event) => {
  resize_iframes();
});
resize_iframes();

const languageParam = getParameterByName('language');
//console.log(languageParam);
const language = (languageParam == null) ? "en" : languageParam;
console.log(language);

const tocUrl = language + "/toc.html";
const indexUrl = language + "/index.html";
console.log(tocUrl);
console.log(indexUrl);

document.querySelector('#navigatorframe').src = tocUrl;
document.querySelector('#contentframe').src = indexUrl ;
