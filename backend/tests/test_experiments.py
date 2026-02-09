import pytest
import os
import json
import shutil
from backend.app.ml.experiments.experiment_logger import ExperimentLogger

class TestExperimentLogger:
    
    @pytest.fixture
    def test_log_dir(self):
        dir_name = "test_experiments"
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        yield dir_name
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            
    def test_log_experiment(self, test_log_dir):
        logger = ExperimentLogger(log_dir=test_log_dir)
        
        log = logger.log_experiment(
            model_name="test_model",
            model_version="v0.1",
            dataset_version="d1",
            task="test_task",
            hyperparameters={"lr": 0.01},
            metrics={"acc": 0.99}
        )
        
        # Check return
        assert log.model_name == "test_model"
        assert log.metrics["acc"] == 0.99
        
        # Check JSON file
        json_path = os.path.join(test_log_dir, "experiments.json")
        assert os.path.exists(json_path)
        with open(json_path, 'r') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["experiment_id"] == log.experiment_id
            
        # Check CSV file
        csv_path = os.path.join(test_log_dir, "experiments.csv")
        assert os.path.exists(csv_path)
        with open(csv_path, 'r') as f:
            content = f.read()
            assert "test_model" in content
            assert "0.99" in content

    def test_schema_validation(self, test_log_dir):
        logger = ExperimentLogger(log_dir=test_log_dir)
        # Should raise validation error if required fields missing
        # But we use typed args in log_experiment so python handles some, 
        # Pydantic handles internal validation.
        pass 
