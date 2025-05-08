// Quiz JavaScript for handling the questionnaire form

document.addEventListener('DOMContentLoaded', function() {
  const skinQuizForm = document.getElementById('skinQuizForm');
  
  if (skinQuizForm) {
    skinQuizForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Get form data
      const formData = new FormData(skinQuizForm);
      
      // Convert form data to object for validation
      const formValues = {};
      for (const [key, value] of formData.entries()) {
        formValues[key] = value;
      }
      
      // Validate form data
      let isValid = true;
      let firstInvalidField = null;
      
      for (const field of skinQuizForm.elements) {
        if (field.tagName === 'SELECT' && field.required && !field.value) {
          isValid = false;
          field.classList.add('is-invalid');
          if (!firstInvalidField) {
            firstInvalidField = field;
          }
        } else {
          field.classList.remove('is-invalid');
        }
      }
      
      if (!isValid) {
        // Scroll to first invalid field
        if (firstInvalidField) {
          firstInvalidField.focus();
          firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }
      
      // Show loading state
      const submitBtn = skinQuizForm.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
      
      // Submit to the server
      fetch('/predict-quiz', {
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
        sessionStorage.setItem('diagnosisType', 'quiz');
        
        // Redirect to the results page
        window.location.href = '/result';
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error processing your responses. Please try again.');
        
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      });
    });
  }
});