from flask import Blueprint, jsonify, request
from textblob import TextBlob
from . import db
from .models import PredictionLog
from .utils import clean_text

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status' : 'active',
        'version' : '1.0.0'
    }), 200
    
@main.route('/analyze', methods=['Post'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'missing "text" field'
            }), 400
            
        original_text = data.get('text')
        cleaned_text = clean_text(original_text)
        
        if not cleaned_text:
            return jsonify({
                'error' : 'No analyzable text found'
            }), 422
            
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            vibe = 'Positive'
        elif polarity < -0.1:
            vibe = 'Negative'
        else:
            vibe = 'Neutral'
            
        new_log = PredictionLog(
            original_text = original_text,
            cleaned_text = cleaned_text,
            polarity = polarity,
            subjectivity = subjectivity,
            vibes = vibe
        )
        try:
            db.session.add(new_log)
            db.session.commit()
            return jsonify({
                'analysis' : {
                    'id': new_log.id,
                    'text' : new_log.original_text,
                    'polarity' : round(new_log.polarity, 2),
                    'vibes': new_log.vibes
                },
                'message' : 'Analysis logged successfully'
                }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error' : str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            'error' : str(e)
        }), 500
        
@main.route('/logs', methods=['GET'])
def get_log():
    try:
        logs = PredictionLog.query.order_by(PredictionLog.timestamp.desc()).limit(10).all()
        all_logs = [{'id': log.id, 'text': log.original_text, 'vibes': log.vibes} for log in logs]
        return jsonify(all_logs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500