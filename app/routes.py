from app.app import app
from flask import request, render_template, jsonify
from celery.result import AsyncResult
from app.tasks import *


@app.route('/')
def default():
    return "Welcome to Report Service"

@app.route('/health')
def health():
    return jsonify({"state":"healthy"})

@app.route('/report', methods=['POST'])
def generate_report():
    async_result = report.delay()
    return jsonify({"report_id":async_result.id})


@app.route('/report/<report_id>')
def get_report(report_id):
    res = AsyncResult(report_id,app=celery)
    return jsonify({"id":res.id,"result":res.result})
