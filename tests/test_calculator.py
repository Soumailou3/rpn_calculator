import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    with app.test_client() as client:
        client.post('/clear')

def test_empty_stack(client):
    """Test que la pile est vide au début"""
    response = client.get('/stack')
    assert response.status_code == 200
    assert json.loads(response.data)['stack'] == []

def test_push_number(client):
    """Test l'ajout d'un nombre dans la pile"""
    response = client.post('/stack', 
                         json={'value': 10})
    assert response.status_code == 201
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [10.0]

def test_push_multiple_numbers(client):
    """Test l'ajout de plusieurs nombres"""
    numbers = [10, 5, 6]
    for num in numbers:
        response = client.post('/stack', 
                             json={'value': num})
        assert response.status_code == 201
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [10.0, 5.0, 6.0]

def test_addition(client):
    """Test l'opération d'addition"""
    client.post('/stack', json={'value': 5})
    client.post('/stack', json={'value': 3})
    
    response = client.post('/operate/+')
    assert response.status_code == 200
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [8.0]

def test_subtraction(client):
    """Test l'opération de soustraction"""
    client.post('/stack', json={'value': 5})
    client.post('/stack', json={'value': 3})
    
    response = client.post('/operate/-')
    assert response.status_code == 200
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [2.0]

def test_multiplication(client):
    """Test l'opération de multiplication"""
    client.post('/stack', json={'value': 4})
    client.post('/stack', json={'value': 3})
    
    response = client.post('/operate/*')
    assert response.status_code == 200
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [12.0]

def test_division(client):
    """Test l'opération de division"""
    client.post('/stack', json={'value': 6})
    client.post('/stack', json={'value': 2})
    
    response = client.post('/operate/')
    assert response.status_code == 200
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == [3.0]

def test_division_by_zero(client):
    """Test la division par zéro"""
    client.post('/stack', json={'value': 6})
    client.post('/stack', json={'value': 0})
    
    response = client.post('/operate/')
    assert response.status_code == 400
    assert b'Division by zero' in response.data

def test_clear_stack(client):
    """Test le nettoyage de la pile"""
    client.post('/stack', json={'value': 5})
    client.post('/stack', json={'value': 3})
    
    response = client.post('/clear')
    assert response.status_code == 200
    
    stack_response = client.get('/stack')
    assert json.loads(stack_response.data)['stack'] == []

