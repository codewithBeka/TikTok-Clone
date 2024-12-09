// Add event listeners to the category links
const categoryLinks = document.querySelectorAll('.category-link');
console.log(categoryLinks)

categoryLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        console.log("click")
        const selectedCategory = event.target.textContent.toLowerCase();
        updateSearchResults(selectedCategory);
    });
});

function updateSearchResults(selectedCategory) {
    // Update the query parameter in the URL
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('query', selectedCategory);
    window.history.pushState({}, '', currentUrl.toString());

    // Fetch the new search results using AJAX
    fetch(`/search?query=${selectedCategory}`)
        .then(response => response.text())
        .then(html => {
            // Replace the search results section with the new HTML
            const searchResultsContainer = document.getElementById('search-results');
            searchResultsContainer.innerHTML = html;
        });
}