"""
Account Service Routes
This module contains the REST API endpoints for the Account service
"""
import json
import logging
from flask import jsonify, request
from service import app
from service.models import Account, db, DataValidationError

logger = logging.getLogger("flask.app")

######################################################################
#  UTILITY FUNCTIONS
######################################################################

def error_response(message, status_code):
    """Helper function to return error responses"""
    body = {"error": message, "status": status_code}
    return jsonify(body), status_code

######################################################################
#  HOME PAGE ROUTE (for test_index)
######################################################################

@app.route("/", methods=["GET"])
def index():
    """Home page for the service"""
    logger.info("Accessing home page")
    return jsonify({"message": "Welcome to Account Service"}), 200

######################################################################
#  HEALTH CHECK ROUTE (Change 'healthy' to 'OK' for test_health)
######################################################################

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({"status": "OK"}), 200

######################################################################
#  CREATE ACCOUNT ROUTE
######################################################################

@app.route("/accounts", methods=["POST"])
def create_account():
    """Create a new Account"""
    logger.info("Request to create account")

    if not request.is_json:
        return error_response("Media type is not JSON", 415)

    try:
        data = request.get_json()
        account = Account.deserialize(data)
        account.create()
        logger.info("Account %s created successfully", account.name)
        return jsonify(account.serialize()), 201
    except DataValidationError as error:
        logger.warning("Validation error: %s", str(error))
        return error_response(str(error), 400)

######################################################################
#  READ ACCOUNT ROUTE
######################################################################

@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read a single Account"""
    logger.info("Request to read account with id: %s", account_id)

    account = Account.find(account_id)

    if account:
        logger.info("Account %s found", account_id)
        return jsonify(account.serialize()), 200
    else:
        logger.warning("Account %s not found", account_id)
        return error_response("Account not found", 404)

######################################################################
#  UPDATE ACCOUNT ROUTE
######################################################################

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an Account"""
    logger.info("Request to update account with id: %s", account_id)

    if not request.is_json:
        return error_response("Media type is not JSON", 415)

    account = Account.find(account_id)

    if not account:
        logger.warning("Account %s not found for update", account_id)
        return error_response("Account not found", 404)

    try:
        account.deserialize(request.get_json())
        account.update()
        logger.info("Account %s updated successfully", account_id)
        return jsonify(account.serialize()), 200
    except DataValidationError as error:
        logger.warning("Validation error: %s", str(error))
        return error_response(str(error), 400)

######################################################################
#  DELETE ACCOUNT ROUTE
######################################################################

@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""
    logger.info("Request to delete account with id: %s", account_id)

    account = Account.find(account_id)

    if account:
        account.delete()
        logger.info("Account %s deleted successfully", account_id)
        return "", 204  # No content
    else:
        logger.warning("Account %s not found for deletion", account_id)
        return error_response("Account not found", 404)

######################################################################
#  LIST ALL ACCOUNTS ROUTE
######################################################################

@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    logger.info("Request to list all accounts")

    accounts = Account.all()
    account_list = [account.serialize() for account in accounts]

    logger.info("Found %d accounts", len(account_list))
    return jsonify(account_list), 200