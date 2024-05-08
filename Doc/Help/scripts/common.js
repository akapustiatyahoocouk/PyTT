//////////
//  Reusable web page fragments - don't duplicate in every page
var navDivHtml =
    `<div class="Logo">
        <image class="LogoImage" src="images/PyTT.png"/>
        TravelBoom
    </div>
    <div class="TopDiv">
        <a class="TopMenu" href="travel_recommendation.html#top">Home</a>
        <a class="TopMenu" href="about_us.html#top">About us</a>
        <a class="TopMenu" href="contact_us.html#top">Contact us</a>
    </div>
    <div class="SearchBar">`;
    if (typeof(includeSearchBarInNavBar) != 'undefined' && includeSearchBarInNavBar) {
        navDivHtml += 
            `<form class="SearchForm">
                <input type="search" id="SearchInput" onkeyup="trackSearchButtonState()">
                <button id="SubmitSearchButton" type="submit" onclick="search()">Search</button>
                <button id="ResetSearchButton" onclick="resetSearchResults()">Reset</button>
            </form>`;
    }
    navDivHtml += `</div>`;
document.querySelector( '#home' ).innerHTML = navDivHtml;
