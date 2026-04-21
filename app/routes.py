from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from app.forms import AddNoteForm, EditNoteForm 
from app import db
from app.models import Note
import json
import sqlalchemy as sa


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

    page = request.args.get('page', 1, type=int)
    query = current_user.notes.select().order_by(Note.timestamp.desc()) #  user = db.session.scalar(sa.select(User).where(User.username=current_user.username))
    notes = db.paginate(query, page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    # notes = db.session.scalars(query)                                   # notes = db.session.scalars(user.posts.select()).all()    

    next_url = url_for('routes.home', page=notes.next_num) \
        if notes.has_next else None
    prev_url = url_for('routes.home', page=notes.prev_num) \
        if notes.has_prev else None

    return render_template('home.html', form=form, notes=notes, next_url=next_url, prev_url=prev_url)


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



@bp.route("/edit-note/<int:note_id>", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None or note.author != current_user:
        abort(404)

    form = EditNoteForm()

    if form.validate_on_submit():
        if len(form.note.data) < 1:
            flash('Note is too short', category='error')

        note.body = form.note.data 
        db.session.commit()
        flash('Your note was updated successfuly!', category='success')
        return redirect(url_for('routes.home'))         
    elif request.method == 'GET':
        form.note.data = note.body

    return render_template('edit_note.html', form=form)           