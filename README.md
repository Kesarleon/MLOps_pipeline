# MLOps E2E (requirements.txt)

Pipeline end-to-end con buenas prácticas: datos → features → train → eval → registro → deploy → monitoreo.

## ⚙️ Stack
- DVC para orquestación de etapas y versionado de datos
- MLflow para tracking y Model Registry
- FastAPI para servir el modelo
- Evidently para monitoreo de drift (batch)
- PyTest + Ruff + pre-commit para calidad

## 🚀 Quickstart

### 1) Clonar e instalar
```bash
git clone <TU_REPO_URL> mlops-e2e && cd mlops-e2e
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/Mac: source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pre-commit install

## 📈 Monitoring

To generate and view the monitoring dashboard, run the DVC pipeline:

```bash
dvc repro
```

This will create the `monitoring/dashboard.html` file, which you can open in your browser to view the Evidently dashboard.

The evaluation metrics are logged to MLflow. To view them, start the MLflow UI:

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

Then, open your browser to `http://localhost:5000` to view the MLflow UI.

To serve the model, run the following command:

```bash
uvicorn service.app:app --host 0.0.0.0 --port 8000
```

## 🚀 Deployment

This project includes a Continuous Deployment (CD) pipeline that automatically deploys the model serving application to Google Cloud Run on every push to the `main` branch.

### GCP Setup

To use the CD pipeline, you need to set up the following in your Google Cloud project:

1.  **Create a GCP Project:** If you don't have one already, create a new GCP project.
2.  **Enable APIs:** Enable the following APIs in your project:
    - Cloud Run API (`run.googleapis.com`)
    - Artifact Registry API (`artifactregistry.googleapis.com`)
    - Identity and Access Management (IAM) API (`iam.googleapis.com`)
3.  **Create an Artifact Registry Repository:** Create a Docker repository in Artifact Registry to store the Docker images.
4.  **Create a Service Account:** Create a service account that will be used by the GitHub Actions workflow to deploy the application.
5.  **Set up Workload Identity Federation:** Follow the official Google Cloud documentation to set up [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) between your GCP project and your GitHub repository. This is the recommended way to authenticate from GitHub Actions to GCP without using long-lived service account keys.
6.  **Grant Permissions:** Grant the following roles to the service account you created:
    - `roles/run.admin`: To deploy to Cloud Run.
    - `roles/artifactregistry.writer`: To push images to Artifact Registry.
    - `roles/iam.serviceAccountUser`: To allow the service account to be impersonated by the Workload Identity Pool.
7.  **Create GitHub Secrets:** Create the following secrets in your GitHub repository:
    - `WIF_PROVIDER`: The full identifier of the Workload Identity Provider.
    - `GCP_SA_EMAIL`: The email of the service account you created.

### Update Workflow Files

Finally, update the `env` section in the `.github/workflows/cd.yml` file with your GCP project details:

```yaml
env:
  GCP_PROJECT_ID: "your-gcp-project-id"
  ARTIFACT_REGISTRY_REPO: "your-artifact-repo"
  CLOUD_RUN_SERVICE_NAME: "your-cloud-run-service"
  GCP_REGION: "your-gcp-region"
```