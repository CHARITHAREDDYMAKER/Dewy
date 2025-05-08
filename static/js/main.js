// Main JavaScript for DEWY application

document.addEventListener('DOMContentLoaded', function() {
  // Initialize Bootstrap components
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
  
  // Image upload modal handling
  const imageMethodBtn = document.getElementById('imageMethodBtn');
  const imageUploadModal = new bootstrap.Modal(document.getElementById('imageUploadModal'));
  const skinImageInput = document.getElementById('skinImage');
  const previewContainer = document.getElementById('previewContainer');
  const imagePreview = document.getElementById('imagePreview');
  const analyzeImageBtn = document.getElementById('analyzeImageBtn');
  
  // Show image upload modal when the image analysis button is clicked
  if (imageMethodBtn) {
    imageMethodBtn.addEventListener('click', function() {
      imageUploadModal.show();
    });
  }
  
  // Preview uploaded image
  if (skinImageInput) {
    skinImageInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          imagePreview.src = e.target.result;
          previewContainer.classList.remove('d-none');
        };
        
        reader.readAsDataURL(this.files[0]);
      }
    });
  }
  
  // Handle image analysis
  if (analyzeImageBtn) {
    analyzeImageBtn.addEventListener('click', function() {
      if (!skinImageInput.files || !skinImageInput.files[0]) {
        alert('Please select an image first.');
        return;
      }
      
      // Create form data
      const formData = new FormData();
      formData.append('file', skinImageInput.files[0]);
      
      // Show loading state
      analyzeImageBtn.disabled = true;
      analyzeImageBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
      
      // Submit to the server
      fetch('/predict-image', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Store result in sessionStorage for the results page
        sessionStorage.setItem('diagnosisResult', JSON.stringify(data));
        sessionStorage.setItem('diagnosisType', 'image');
        
        // Redirect to the results page
        window.location.href = '/result';
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error analyzing image. Please try again.');
        
        // Reset button state
        analyzeImageBtn.disabled = false;
        analyzeImageBtn.innerHTML = 'Analyze Image';
      });
    });
  }
});