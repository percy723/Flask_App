# main.py

from flask import Flask, Blueprint, render_template, request, redirect ,url_for
from flask_login import login_required, current_user
from cryptography.fernet import Fernet #for Encryption/ Decryption
from .models import Credential
from . import db

main = Blueprint('main', __name__)

encrypt_key = 'sk'

@main.route('/')
def index():
    return render_template('index.html')

# //-----------[SUBPAGE] profile-----------//

@main.route('/profile')
@login_required
def profile():
    # filter the password key belongs to specific logged in user 
    credential_list = Credential.query.filter_by(user_id=current_user.id).all()

    return render_template('profile.html', name=current_user.name, credential_list=credential_list, is_admin = current_user.is_admin)

   
@main.route('/profile/copy', methods=['POST'])
@login_required
def copy():
    receivedData = request.get_json()
    receivedId = receivedData['id']
    queryCred = Credential.query.filter_by(id=receivedId).first()

    f = Fernet(encrypt_key)
    k = queryCred.credential_key
    bk = bytes(k) #change into bytes first
    decrypt_key = f.decrypt(bk)
    return(decrypt_key)

# Username
@main.route('/profile/edit_key_name', methods=['POST'])
@login_required
def edit_key_name():
    receivedData = request.get_json()
    receivedId = receivedData['id']
    queryCred = Credential.query.filter_by(id=receivedId).first()
    queryCred.credential_name = receivedData['key_name']
    db.session.commit()
    return "Edit Username OK"

# Description
@main.route('/profile/edit_key_description', methods=['POST'])
@login_required
def edit_key_desc():
    receivedData = request.get_json()
    receivedId = receivedData['id']
    queryCred = Credential.query.filter_by(id=receivedId).first()
    queryCred.credential_description = receivedData['key_desc']
    db.session.commit()
    return "Edit Description OK"

# Password
@main.route('/profile/edit_key', methods=['POST'])
@login_required
def edit_key():
    receivedData = request.get_json()
    receivedId = receivedData['id']
    queryCred = Credential.query.filter_by(id=receivedId).first()
    new_credential_key = receivedData['key'] # the new edited key

    f = Fernet(encrypt_key)
    b_new_credential_key = bytes(new_credential_key) #change to byte
    new_encrypted_credential_key = f.encrypt(b_new_credential_key) #encrypt

    # ORM SQL: Assign the new value to that queried row
    queryCred.credential_key = new_encrypted_credential_key

    db.session.commit()
    return "Edit Password OK"


@main.route('/profile/delete', methods=['POST'])
@login_required
def delete():
    receivedData = request.get_json()
    receivedId = receivedData['id']
    queryCred = Credential.query.filter_by(id=receivedId).delete()
    db.session.commit()
    return "Deleted"

# //-----------[SUBPAGE] savekey------------//

@main.route('/savekey')
@login_required
def savekey():
    return render_template('profile_credential.html')

@main.route('/savekey', methods=['POST'])
@login_required
def savekey_post():

    f = Fernet(encrypt_key)

    credential_name = request.form.get('key_name')
    credential_key = request.form.get('key_content')
    credential_description = request.form.get('key_description')

    # encrypt save key
    # change saving data to bytes:  bytes('example', encoding='utf-8')
    b_credential_key = bytes(credential_key)
    encrypted_credential_key = f.encrypt(b_credential_key)
 
    # new_key = Credential(credential_name=credential_name, credential_key=credential_key, user_id=current_user.id)
    new_key = Credential(credential_name=credential_name, credential_key=encrypted_credential_key, credential_description = credential_description , user_id=current_user.id)

    db.session.add(new_key)
    db.session.commit()

    return redirect(url_for('main.profile'))