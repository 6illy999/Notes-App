from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user  
from app.forms import AddNoteForm 
from app import db
from app.models import Note
import json


bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def home():

    form = AddNoteForm()
    if form.validate_on_submit():
        if len(form.note.data) < 1:
            flash('NNote is too short', category='error')
        #print ("FORM VALID")
        note = Note(body=form.note.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Your note was added successfuly!', category='success')
        return redirect(url_for('routes.home'))

    query = current_user.notes.select().order_by(Note.timestamp.desc())    
    notes = db.session.scalars(query)

    return render_template('home.html', form=form, notes=notes)


@bp.route("/delete-note", methods=['GET', 'POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.author == current_user:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
    return jsonify({})