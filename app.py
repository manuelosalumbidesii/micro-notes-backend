from flask import Flask, request, jsonify
import uuid
from util import read_notes, write_notes

app = Flask(__name__)


@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = read_notes()
    return jsonify(notes), 200


@app.route('/api/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    notes = read_notes()
    note = next((n for n in notes if n['id'] == note_id), None)
    if note:
        return jsonify(note), 200
    return jsonify({'error': 'Note not found'}), 404


@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json(force=True)
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Invalid input'}), 400

    new_note = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'content': data['content']
    }
    notes = read_notes()
    notes.append(new_note)
    write_notes(notes)
    return jsonify(new_note), 201


@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    notes = read_notes()
    new_notes = [n for n in notes if n['id'] != note_id]
    if len(notes) == len(new_notes):
        return jsonify({'error': 'Note not found'}), 404
    write_notes(new_notes)
    return jsonify({'message': 'Note deleted'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
