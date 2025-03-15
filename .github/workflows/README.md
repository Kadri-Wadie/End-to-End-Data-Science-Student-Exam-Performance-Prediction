# Python Azure Web App Deployment

This project demonstrates a CI/CD pipeline using GitHub Actions to automatically build and deploy a Python application to **Azure Web App**. The workflow is defined in `.github/workflows/main_studentssperformance3.yml`.

## Workflow Overview
### Purpose
- **Automated Deployment**: Deploys the app to Azure whenever code is pushed to the `main` branch.
- **Build Process**: Sets up Python 3.7, installs dependencies, and prepares artifacts.
- **Security**: Uses GitHub Secrets to securely store Azure credentials.

### Key Features
- **Triggers**: Runs on `push` to `main` or manually via GitHub Actions UI (`workflow_dispatch`).
- **Artifact Handling**: Excludes unnecessary files (e.g., `venv/`) during deployment.
- **Environment**: Targets the `Production` environment in Azure.

## Prerequisites
1. **Azure Web App**: Set up an Azure Web App instance named `studentssperformance3`.
2. **GitHub Secrets**: Store your Azure publish profile credentials in GitHub Secrets under `AZUREAPPSERVICE_PUBLISHPROFILE_...`.

## How It Works
1. **Build Job**:
   - Checks out the repository.
   - Configures Python 3.7 and a virtual environment.
   - Installs dependencies from `requirements.txt`.
   - Uploads the app code (excluding `venv/`) as an artifact.
   
2. **Deploy Job**:
   - Downloads the artifact from the `build` job.
   - Deploys the code to Azure Web App using stored credentials.

## Usage
1. Push code to the `main` branch to trigger automatic deployment.
2. Monitor workflow runs in the GitHub Actions tab.
3. Access the deployed app at your Azure Web App URL.
