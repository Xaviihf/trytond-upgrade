OPERATIONS = [
    {
        "name": "Use NULL value for empty foreign key with:",
        "version": "7.2",
        "modules": None,
        "sql": """
            UPDATE "ir_ui_view" SET "model" = NULL WHERE "model" = '';
            UPDATE "ir_action_act_window" SET "res_model" = NULL WHERE "res_model" = '';
            UPDATE "ir_action_wizard" SET "model" = NULL WHERE "model" = '';
            UPDATE "ir_action_report" SET "model" = NULL WHERE "model" = '';
            UPDATE "ir_action_report" SET "module" = NULL WHERE "module" = '';
            UPDATE "ir_translation" SET "module" = NULL WHERE "module" = '';
        """,
    },
    {
        "name": "Rename columns of ir.model and ir.model.field:",
        "version": "7.6",
        "modules": None,
        "sql": """
            ALTER TABLE IF EXISTS "ir_model" RENAME COLUMN "name" TO "string";
            ALTER TABLE IF EXISTS "ir_model" RENAME COLUMN "model" TO "name";
            ALTER TABLE IF EXISTS "ir_model_field" RENAME COLUMN "field_description" TO "string";
        """,
    },
    {
        "name": "Remove NOT NULL to before_carrier and after_carrier:",
        "version": "7.8",
        "modules": ["carrier_carriage"],
        "sql": """
            ALTER TABLE "incoterm_incoterm" ALTER COLUMN "before_carrier" DROP NOT NULL;
            ALTER TABLE "incoterm_incoterm" ALTER COLUMN "after_carrier" DROP NOT NULL;
        """,
    },
]