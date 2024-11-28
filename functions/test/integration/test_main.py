from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from datetime import datetime
import pytest
import os

from test.mock_equipment import create_valid_equipments
from main import update_equipments_location

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['equipment'].insert_many(create_valid_equipments())
    yield db
    db['equipment'].delete_many({})

# Testando função quando mudar a localização
@patch('main.datetime')
@patch('database.repositories.equipment_repository.datetime')
@patch('main.EquipmentDAO.get_all_esp_id')
@patch('main.requests.get')
@pytest.mark.asyncio
async def test_update_equipments_location_integration_success(mock_get, mock_get_all_esp_id, mock_repository_datetime_now, mock_service_datetime_now):

    mock_get_all_esp_id.return_value = [{'esp_id': '1111'}]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = 'new_room'
    mock_get.return_value = mock_response

    # Mock do c_date (data da ultima atualização)
    mock_repository_datetime_now.now.return_value = datetime(2024,11,10,20,30,00)
    mock_service_datetime_now.now.return_value = datetime(2024,11,10,20,30,00)

    await update_equipments_location()

    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    equipment_data = db['equipment'].find_one({'esp_id': '1111'}, {'c_room': 1, 'c_date': 1, 'initial_date': 1,'historic': 1})

    assert equipment_data['c_date'] == datetime(2024,11,10,20,30,00)
    assert equipment_data['initial_date'] == datetime(2024,11,10,20,30,00)
    assert equipment_data['c_room'] == 'new_room'
    assert equipment_data['historic'][3]['room'] == 'Emergency'
    assert equipment_data['historic'][3]['initial_date'] == datetime(2024,8,8,19,54,14)