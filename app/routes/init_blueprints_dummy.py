# app/routes/patient.py
from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
bp = Blueprint('patient', __name__, url_prefix='/patient')

# app/routes/doctor.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
bp = Blueprint('doctor', __name__, url_prefix='/doctor')

# app/routes/pharmacist.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
bp = Blueprint('pharmacist', __name__, url_prefix='/pharmacy')

# app/routes/chat.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
bp = Blueprint('chat', __name__, url_prefix='/chat')
