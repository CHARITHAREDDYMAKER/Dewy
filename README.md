STEPS TO RUN PROJECT LOCALLY
  1)Clone the repo:
    git clone https://github.com/CHARITHAREDDYMAKER/DEWY.git
    cd DEWY
  2)Install dependencies:
    pip install flask scikit-learn tensorflow
  3)Run the backend (Flask):
    cd SkinDiseaseAssistant
    python app.py
  4)Open in Browser:
    http://localhost:5000

WE UPLOADED SRS,SDD,PROJECT PPT AS FILES IN GITHUB


NOTE FOR EVALUATION:
⚠️ GITHUB UPLOAD ISSUE (Important for Evaluation)
While uploading our project to GitHub, we encountered the following issue:

❌ "File exceeds GitHub’s 25MB limit"
GitHub restricts individual file sizes to a maximum of 25MB. Our trained machine learning model files (.pkl and .keras) exceeded this limit.

✅ How We Solved It
We used Git Large File Storage (Git LFS) to upload large model files.

If you're cloning this repository and notice missing model files:

Make sure Git LFS is installed on your system. You can install it from https://git-lfs.com.

Then run:
git lfs install
git lfs pull

🧰 Backup Option
To avoid evaluation delays:

We can also provide a Google Drive link or a ZIP file containing the complete project (including model files).

Please contact us if model files are missing or you face difficulty running the project.
