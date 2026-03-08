"""
Test cases for Account Service
This module ensures the REST API endpoints function correctly
using Test-Driven Development (TDD) practices.
"""
import json
from service import app
from service.models import Account, db, DataValidationError
from nose.tools import assert_equal, assert_true, assert_false, assert_raises,assert_in
import logging

# Disable noisy logging for cleaner test output
logging.disable(logging.CRITICAL)

class TestAccountService:
    """Test cases for Account Service"""
    
    def setup(self):
        """
        Run before each test case.
        Configures the app for testing mode and initializes an in-memory database.
        """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Override to SQLite in-memory for fast, isolated tests
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        
        self.app = app.test_client()
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # Create tables
        self.reset_database()
    
    def teardown(self):
        """Run after each test case to clean up."""
        db.session.remove()
        db.drop_all()
    
    def reset_database(self):
        """Clear all accounts before every test."""
        Account.query.delete()
        db.session.commit()
    
    ######################################################################
    #  H E A L T H   C H E C K   T E S T S
    ######################################################################
    
    def test_health_check(self):
        """Should return healthy status when app is running"""
        response = self.app.get("/health")
        assert_equal(response.status_code, 200)
        data = json.loads(response.data)
        assert_equal(data["status"], "OK")

    ######################################################################
    #  R E A D   A C C O U N T   T E S T S
    ######################################################################
    
    def test_read_account_success(self):
        """Should read an existing account successfully"""
        # SETUP
        account = Account(name="John Doe", email="john@example.com", address="123 Main St")
        account.create()
        account_id = account.id
        
        # EXECUTE
        response = self.app.get(f"/accounts/{account_id}")
        
        # ASSERT
        assert_equal(response.status_code, 200)
        data = json.loads(response.data)
        assert_equal(data["name"], "John Doe")
        assert_equal(data["email"], "john@example.com")
        assert_equal(data["address"], "123 Main St")
    
    def test_read_account_not_found(self):
        """Should return 404 when account does not exist"""
        # EXECUTE
        response = self.app.get("/accounts/99999")
        
        # ASSERT
        assert_equal(response.status_code, 404)
        data = json.loads(response.data)
        assert_equal(data["error"], "Account not found")

    ######################################################################
    #  L I S T   A C C O U N T S   T E S T S
    ######################################################################
    
    def test_list_accounts_success(self):
        """Should list all existing accounts"""
        # SETUP
        Account(name="John Doe", email="john@example.com", address="123 Main St").create()
        Account(name="Jane Smith", email="jane@example.com", address="456 Oak Ave").create()
        
        # EXECUTE
        response = self.app.get("/accounts")
        
        # ASSERT
        assert_equal(response.status_code, 200)
        data = json.loads(response.data)
        assert_true(isinstance(data, list))
        assert_equal(len(data), 2)
    
    def test_list_accounts_empty(self):
        """Should return empty list when no accounts exist"""
        # RESET
        self.reset_database()
        
        # EXECUTE
        response = self.app.get("/accounts")
        
        # ASSERT
        assert_equal(response.status_code, 200)
        data = json.loads(response.data)
        assert_equal(len(data), 0)

    ######################################################################
    #  U P D A T E   A C C O U N T   T E S T S
    ######################################################################
    
    def test_update_account_success(self):
        """Should update an existing account"""
        # SETUP
        account = Account(name="John Doe", email="john@example.com", address="123 Main St")
        account.create()
        account_id = account.id
        
        # UPDATE DATA
        update_data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "address": "789 New Street",
            "phone_number": "555-0199"
        }
        
        # EXECUTE
        response = self.app.put(
            f"/accounts/{account_id}",
            json=update_data,
            content_type="application/json"
        )
        
        # ASSERT
        assert_equal(response.status_code, 200)
        data = json.loads(response.data)
        assert_equal(data["name"], "Jane Doe")
        assert_equal(data["email"], "jane.doe@example.com")
        
        # VERIFY IN DATABASE
        updated_account = Account.find(account_id)
        assert_equal(updated_account.name, "Jane Doe")
    
    def test_update_account_not_found(self):
        """Should return 404 when updating non-existent account"""
        update_data = {"name": "Test User"}
        response = self.app.put(
            "/accounts/99999",
            json=update_data,
            content_type="application/json"
        )
        assert_equal(response.status_code, 404)
    
    def test_update_account_invalid_data(self):
        """Should return 400 when update data is invalid (missing required fields)"""
        # SETUP
        account = Account(name="John Doe", email="john@example.com", address="123 Main St")
        account.create()
        account_id = account.id
        
        # UPDATE DATA (Missing 'name' which is required)
        update_data = {"email": "new@example.com"}
        
        # EXECUTE
        response = self.app.put(
            f"/accounts/{account_id}",
            json=update_data,
            content_type="application/json"
        )
        
        # ASSERT
        assert_equal(response.status_code, 400)
        data = json.loads(response.data)
        assert_equal(data["status"], 400)

    ######################################################################
    #  D E L E T E   A C C O U N T   T E S T S
    ######################################################################
    
    def test_delete_account_success(self):
        """Should delete an existing account"""
        # SETUP
        account = Account(name="John Doe", email="john@example.com", address="123 Main St")
        account.create()
        account_id = account.id
        
        # EXECUTE
        response = self.app.delete(f"/accounts/{account_id}")
        
        # ASSERT
        assert_equal(response.status_code, 204)
        
        # VERIFY GONE
        deleted_account = Account.find(account_id)
        assert_false(deleted_account)
    
    def test_delete_account_not_found(self):
        """Should return 404 when deleting non-existent account"""
        response = self.app.delete("/accounts/99999")
        assert_equal(response.status_code, 404)

    ######################################################################
    #  T E S T   S E C U R I T Y   H E A D E R S
    ######################################################################
    
    def test_security_headers(self):
        """Should return X-Frame-Options header via Talisman"""
        response = self.app.get("/health")
        
        # Check for Frame options protection
        assert_true(response.headers.get("X-Frame-Options"))
        # Check for Strict Transport Security (optional depending on config)
        assert_in("Content-Security-Policy", response.headers)
    
    def test_cors_enabled(self):
        """Should allow Cross-Origin requests"""
        # Send an OPTIONS request (preflight)
        response = self.app.options(
            "/accounts",
            headers={"Origin": "http://localhost:3000"}
        )
        # Verify CORS headers are present
        assert_in(response.status_code, [200, 204])  # Accept either
        assert_in("Access-Control-Allow-Origin", response.headers)