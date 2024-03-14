# Expense Sharing App


#List of APIs:


1. List all Users
        
        curl --location 'http://localhost:8000/users/list/'

2. Add a User

        curl --location 'http://localhost:8000/users/add/' \
        --header 'Content-Type: application/json' \
        --data-raw '{"name": "user5", "email": "user5@gmail.com", "mobile_number": "1231231230"}'


3. Show Balances

        curl --location 'http://localhost:8000/expenses/show_balances/'

4. Show expense for specific User

        curl --location 'http://localhost:8000/expenses/user_expenses/79ACD/'

    79ACD --> sample userid

5. Add Expense

        5.1 Expense Type - Equal

        curl --location 'http://localhost:8000/expenses/add_expense/' \
            --header 'Content-Type: application/json' \
            --data '{"user_id": "79ACD", "amount": 100.00, "expense_type": "EQUAL"}
            '

            
        5.2 Expense Type - Exact

        curl --location 'http://localhost:8000/expenses/add_expense/' \
            --header 'Content-Type: application/json' \
            --data '
            {
            "user_id": "79ACD",
            "amount": 50.00,
            "expense_type": "EXACT",
            "shares": {
                "27DED": 20.00,
                "ACEB7": 30.00
            }
            }
            '

        5.3 Expense Type - Percent

        curl --location 'http://localhost:8000/expenses/add_expense/' \
            --header 'Content-Type: application/json' \
            --data '
            {
            "user_id": "27DED",
            "amount": 200.00,
            "expense_type": "PERCENT",
            "shares": {
                "27DED": 50,
                "ACEB7": 50
            }
            }
            '