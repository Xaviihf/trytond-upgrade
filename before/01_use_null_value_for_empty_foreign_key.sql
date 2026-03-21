UPDATE "ir_ui_view" SET "model" = NULL WHERE "model" = '';
UPDATE "ir_action_act_window" SET "res_model" = NULL WHERE "res_model" = '';
UPDATE "ir_action_wizard" SET "model" = NULL WHERE "model" = '';
UPDATE "ir_action_report" SET "model" = NULL WHERE "model" = '';
UPDATE "ir_action_report" SET "module" = NULL WHERE "module" = '';
UPDATE "ir_translation" SET "module" = NULL WHERE "module" = '';