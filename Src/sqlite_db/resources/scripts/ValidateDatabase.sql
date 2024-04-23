SELECT [pk], [object_type_name] FROM [objects];
SELECT [pk], [enabled], [real_name], [inactivity_timeout], 
       [ui_locale], [email_addresses] FROM [users];
SELECT [pk], [enabled], [login], [password_hash],
       [is_administrator],
       [can_manage_users],
       [can_manage_stock_items],
       [can_manage_beneficiaries],
       [can_manage_workloads],
       [can_manage_public_activities],
       [can_manage_public_tasks],
       [can_manage_private_activities],
       [can_manage_private_tasks],
       [can_log_work],
       [can_log_events],
       [can_generate_reports],
       [can_backup_and_restore],
       [email_addresses] FROM [accounts];


