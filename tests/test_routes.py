def test_health_check(client):
    """Test that the health check returns 200 OK."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'active'

def test_analyze_sentiment_positive(client):
    """Test a positive sentiment."""
    response = client.post('/analyze', json={'text': 'I love writing code!'})
    assert response.status_code == 201
    assert response.json['analysis']['vibes'] == 'Positive'
    assert response.json['message'] == 'Analysis logged successfully'

def test_analyze_sentiment_negative(client):
    """Test a negative sentiment."""
    response = client.post('/analyze', json={'text': 'This error is terrible.'})
    assert response.status_code == 201
    assert response.json['analysis']['vibes'] == 'Negative'

def test_analyze_empty_input(client):
    """Test error handling for empty input."""
    response = client.post('/analyze', json={'text': ''})
    assert response.status_code == 422
    assert "error" in response.json