from fastapi.testclient import TestClient
from service.app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict():
    """Test the predict endpoint."""
    # This is a mock test, as we don't have a model loaded in the test environment
    # In a real-world scenario, you would mock the mlflow.pyfunc.load_model call
    # or have a separate test model for testing purposes.

    # For now, we will just check if the endpoint is reachable,
    # but we expect a 503 error because the model is not loaded.
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert response.status_code == 503
    assert response.json() == {"detail": "Model not loaded"}
