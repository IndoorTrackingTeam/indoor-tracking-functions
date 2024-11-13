import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from main import update_equipments_location, update_database, UpdateEquipmentsHistoric, UpdateEquipmentsCurrentRoom

# Teste para o fluxo principal de sucesso
@patch('main.EquipmentDAO.get_all_esp_id')
@patch('main.requests.get')
def test_update_equipments_location_success(mock_get, mock_get_all_esp_id):
    
    mock_get_all_esp_id.return_value = [{'esp_id': '12345'}]
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = 'new_room'
    mock_get.return_value = mock_response

    update_equipments_location()

    mock_get.assert_called_with('https://run-machine-learning-api-prod-131050301176.us-east1.run.app/model-training/get-esp-position?esp_id=12345')


# Teste para verificar se as funções do banco de dados não estão sendo chamadas
@patch('main.EquipmentDAO')
@patch('main.requests.get')
def test_update_equipments_location_http_error(mock_get, MockEquipmentDAO):
    
    mock_equipmentDAO_instance = MockEquipmentDAO.return_value
    mock_equipmentDAO_instance.get_all_esp_id.return_value = [{'esp_id': '12345'}]

    mock_response = MagicMock()
    mock_response.status_code = 500  
    mock_response.json.return_value = ''
    mock_get.return_value = mock_response

    update_equipments_location()

    mock_equipmentDAO_instance.get_current_room_and_date.assert_not_called()
    mock_equipmentDAO_instance.update_database.assert_not_called()
    

# Teste para garantir que update_historic e update_current_room são chamados corretamente
def test_update_database_success():
   
    mock_equipmentDAO = MagicMock()
    
    esp_id = '12345'
    new_current_room = 'new_room'
    num_try = 0

    update_database(mock_equipmentDAO, new_current_room, esp_id, num_try)

    date_key = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mock_equipmentDAO.update_historic.assert_called_once_with(UpdateEquipmentsHistoric(
        esp_id=esp_id, room=new_current_room, initial_date=date_key
    ))
    mock_equipmentDAO.update_current_room.assert_called_once_with(UpdateEquipmentsCurrentRoom(
        esp_id=esp_id, c_room=new_current_room
    ), date_key)

# Teste para verificar o tratamento de exceção
def test_update_database_exception():
    mock_equipmentDAO = MagicMock()
    mock_equipmentDAO.update_historic.side_effect = Exception("Database connection error")

    esp_id = '12345'
    new_current_room = 'new_room'
    num_try = 0

    update_database(mock_equipmentDAO, new_current_room, esp_id, num_try)

    mock_equipmentDAO.update_historic.assert_called_once()
    mock_equipmentDAO.update_current_room.assert_not_called() 
