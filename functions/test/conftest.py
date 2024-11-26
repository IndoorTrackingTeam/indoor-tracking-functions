import os
import pytest

# Fixture para configurar o ambiente de QA
@pytest.fixture(scope="session", autouse=True)
def set_qa_environment():
    os.environ['DB_NAME'] = "indoor_db_QA"
    