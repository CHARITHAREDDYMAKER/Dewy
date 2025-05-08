// Results page JavaScript for displaying diagnosis results

document.addEventListener('DOMContentLoaded', function() {
  // Elements on the results page
  const diagnosisTitle = document.getElementById('diagnosisTitle');
  const confidenceBar = document.getElementById('confidenceBar');
  const confidenceScore = document.getElementById('confidenceScore');
  const diagnosisDescription = document.getElementById('diagnosisDescription');
  const productsList = document.getElementById('productsList');
  const dietList = document.getElementById('dietList');
  const uploadedImageContainer = document.getElementById('uploadedImageContainer');
  const uploadedImage = document.getElementById('uploadedImage');
  const saveResultsBtn = document.getElementById('saveResultsBtn');
  
  // Check if we have diagnosis results in session storage
  const diagnosisResult = JSON.parse(sessionStorage.getItem('diagnosisResult') || '{}');
  const diagnosisType = sessionStorage.getItem('diagnosisType') || '';
  
  if (Object.keys(diagnosisResult).length === 0) {
    // No data found
    diagnosisTitle.textContent = 'No diagnosis data found';
    diagnosisDescription.innerHTML = '<div class="alert alert-warning">Please complete a diagnosis using either the image upload or questionnaire method.</div>';
    
    // Hide confidence indicators
    confidenceBar.style.width = '0%';
    confidenceScore.textContent = 'N/A';
  } else {
    // Display the diagnosis data
    const disease = diagnosisResult.disease || 'Unknown';
    const description = diagnosisResult.description || 'No description available.';
    const confidenceValue = diagnosisResult.confidence_score || '0%';
    const confidenceNum = parseInt(confidenceValue) || 0;
    const products = diagnosisResult.product_recommendations || [];
    const dietRecommendations = diagnosisResult.diet_recommendations || [];
    
    // Set the diagnosis title and confidence
    diagnosisTitle.textContent = `Diagnosis: ${disease.charAt(0).toUpperCase() + disease.slice(1)}`;
    confidenceBar.style.width = confidenceValue;
    confidenceScore.textContent = confidenceValue;
    
    // Set confidence bar color based on value
    if (confidenceNum >= 80) {
      confidenceBar.className = 'progress-bar bg-success';
    } else if (confidenceNum >= 60) {
      confidenceBar.className = 'progress-bar bg-info';
    } else if (confidenceNum >= 40) {
      confidenceBar.className = 'progress-bar bg-warning';
    } else {
      confidenceBar.className = 'progress-bar bg-danger';
    }
    
    // Set description
    diagnosisDescription.innerHTML = `<h4>About This Condition</h4><p>${description}</p>`;
    
    // Set product recommendations
    if (products.length > 0) {
      productsList.innerHTML = '';
      products.forEach(product => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `<strong>${product.name}</strong><p>${product.description || ''}</p>`;
        productsList.appendChild(li);
      });
    } else {
      productsList.innerHTML = '<li class="list-group-item text-center">No specific product recommendations available.</li>';
    }
    
    // Set diet recommendations
    if (dietRecommendations.length > 0) {
      dietList.innerHTML = '';
      dietRecommendations.forEach(diet => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `<strong>${diet.name}</strong><p>${diet.description || ''}</p>`;
        dietList.appendChild(li);
      });
    } else {
      dietList.innerHTML = '<li class="list-group-item text-center">No specific dietary recommendations available.</li>';
    }
    
    // Show image if available from image diagnosis
    if (diagnosisType === 'image' && diagnosisResult.image_path) {
      uploadedImage.src = `/uploads/${diagnosisResult.image_path.split('/').pop()}`;
      uploadedImageContainer.classList.remove('d-none');
    }
  }
  
  // Handle saving the results
  if (saveResultsBtn) {
    saveResultsBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      try {
        // Create a PDF-like formatted result (this is simplified - in production you'd use a proper PDF generation library)
        const printWindow = window.open('', '_blank');
        
        if (!printWindow) {
          alert('Please allow popups to save your results.');
          return;
        }
        
        let htmlContent = `
          <!DOCTYPE html>
          <html lang="en">
          <head>
            <meta charset="UTF-8">
            <title>DEWY Skin Diagnosis Results</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; }
              .header { text-align: center; margin-bottom: 30px; }
              .diagnosis { margin-bottom: 20px; }
              .section { margin-bottom: 20px; }
              .recommendations { margin-top: 30px; }
              .footer { margin-top: 50px; text-align: center; font-size: 12px; }
              h1 { color: #4caf50; }
              h2 { color: #2196f3; }
              .confidence { display: inline-block; width: 100%; background-color: #f0f0f0; height: 20px; }
              .confidence-bar { height: 100%; background-color: #4caf50; }
              table { width: 100%; border-collapse: collapse; margin: 20px 0; }
              table, th, td { border: 1px solid #ddd; }
              th, td { padding: 12px; text-align: left; }
              th { background-color: #f2f2f2; }
            </style>
          </head>
          <body>
            <div class="header">
              <h1>DEWY Skin Condition Diagnosis</h1>
              <p>Date: ${new Date().toLocaleDateString()}</p>
            </div>
            
            <div class="diagnosis">
              <h2>${diagnosisTitle.textContent}</h2>
              <p>Confidence: ${confidenceScore.textContent}</p>
              <div class="confidence">
                <div class="confidence-bar" style="width: ${confidenceScore.textContent}"></div>
              </div>
            </div>
            
            <div class="section">
              <h3>About This Condition</h3>
              <p>${diagnosisDescription.textContent}</p>
            </div>
            
            <div class="recommendations">
              <h3>Recommended Products</h3>
              <table>
                <tr><th>Product</th><th>Description</th></tr>
                ${Array.from(productsList.children).map(li => {
                  const name = li.querySelector('strong')?.textContent || '';
                  const desc = li.querySelector('p')?.textContent || '';
                  return `<tr><td>${name}</td><td>${desc}</td></tr>`;
                }).join('')}
              </table>
              
              <h3>Dietary Recommendations</h3>
              <table>
                <tr><th>Food/Diet</th><th>Description</th></tr>
                ${Array.from(dietList.children).map(li => {
                  const name = li.querySelector('strong')?.textContent || '';
                  const desc = li.querySelector('p')?.textContent || '';
                  return `<tr><td>${name}</td><td>${desc}</td></tr>`;
                }).join('')}
              </table>
            </div>
            
            <div class="footer">
              <p>This diagnosis is provided by DEWY using AI technology. Always consult with a healthcare professional for medical advice.</p>
              <p>&copy; 2025 DEWY. All rights reserved.</p>
            </div>
          </body>
          </html>
        `;
        
        printWindow.document.write(htmlContent);
        printWindow.document.close();
        
        // Allow the browser to render the content before printing
        setTimeout(() => {
          printWindow.print();
        }, 500);
        
      } catch (error) {
        console.error('Error saving results:', error);
        alert('An error occurred while saving your results. Please try again.');
      }
    });
  }
});