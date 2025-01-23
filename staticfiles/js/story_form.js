document.getElementById('id_images').addEventListener('change', function(e) {
    const container = document.getElementById('imagePreviewContainer');
    const files = e.target.files;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'relative group';
                div.innerHTML = `
                    <img src="${e.target.result}" alt="Image Preview" class="w-full h-32 object-cover rounded-lg">
                    <button type="button" onclick="removeImage(this)" 
                            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                `;
                container.appendChild(div);
            };
            reader.readAsDataURL(file);
        }
    }
});

function removeImage(button) {
    const imageContainer = button.closest('.relative');
    if (imageContainer) {
        const imageId = button.dataset.imageId;
        if (imageId) {
            // If this is an existing image, add it to a list of images to be removed
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'remove_images';
            input.value = imageId;
            document.getElementById('storyForm').appendChild(input);
        }
        imageContainer.remove();
    }
}
