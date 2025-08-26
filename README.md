# MLOps E2E (requirements.txt)

Pipeline end-to-end con buenas prácticas: datos → features → train → eval → registro → deploy → monitoreo.

## ⚙️ Stack
- DVC para orquestación de etapas y versionado de datos
- MLflow (UI opcional vía Docker) para tracking y Model Registry
- FastAPI para servir el modelo (Docker)
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
docker-compose up mlflow
```

Then, open your browser to `http://localhost:5000` to view the MLflow UI.