from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_jwt_extended import jwt_required, get_jwt_identity

main = Blueprint('main', __name__)


@main.route('/dashboard', methods=["GET", "POST"])
@jwt_required
def dashboard():
    flash('Hello World')
    return render_template('dashboard.html')