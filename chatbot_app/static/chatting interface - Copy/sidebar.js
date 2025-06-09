// Update JavaScript for sidebar
const sidebar = document.querySelector('.sidebar');
const sidebarToggle = document.querySelector('#sidebar-toggle');

// Toggle sidebar
sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking outside
document.addEventListener('click', (event) => {
    if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});

// Handle sidebar item clicks
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', () => {
        const hiddenPrompt = item.dataset.prompt;
        promptInput.value = `As a language learning expert, ${hiddenPrompt}. Include examples and exercises.`;
        promptForm.dispatchEvent(new Event('submit'));
    });
});



