// static/js/navigation.js
function navigateToProducts(category) {
    try {
        const baseUrl = window.location.origin;
        let url = `${baseUrl}/products`;
        
        if (category) {
            url += `?category=${encodeURIComponent(category)}`;
        }
        
        window.location.href = url;
        return false; // Prevent default link behavior
    } catch (error) {
        console.error('Navigation error:', error);
        return true; // Allow default link behavior as fallback
    }
}

// Debug function to check if script is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Navigation script loaded');
    
    // Add click handlers to all category cards
    document.querySelectorAll('.category-card').forEach(card => {
        console.log('Found category card:', card);
    });
});