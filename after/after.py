OPERATIONS = [
    {
        "name": "Remove open_lines button:",
        "version": "7.4",
        "modules": ["product_price_list", "product_price_list_dates"],
        "sql": """
            DELETE FROM "ir_model_button" WHERE "name" = 'open_lines' AND "model" = 'product.price_list';
        """,
    },
    {
        "name": "Fill the internal transit location:",
        "version": "7.6",
        "modules": ["stock"],
        "script": None, # TODO: Support scripts
        "sql": None,
    },
    {
        "name": "Invert account_budget_line.amount sign:",
        "version": "7.6",
        "modules": ["account_budget"],
        "sql": """
            UPDATE "account_budget_line" SET amount = -amount;
        """,
    },
    {
        "name": "Invert analytic_budget.amount sign:",
        "version": "7.6",
        "modules": ["analytic_budget"],
        "sql": """
            UPDATE "analytic_account_budget_line" SET amount = -amount;
        """,
    },
    {
        "name": "Fill the address of validated mandates with default value:",
        "version": "7.6",
        "modules": ["account_payment_sepa"],
        "script": None, # TODO: Support scripts
        "sql": None,
    },
]