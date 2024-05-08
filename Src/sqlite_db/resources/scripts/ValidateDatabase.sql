CREATE TEMP TABLE [constraints]
(
    [condition] INTEGER NOT NULL CHECK([condition] = 0)
);

INSERT INTO [constraints] SELECT COUNT(NAME)-2 FROM PRAGMA_TABLE_INFO('objects');
SELECT [pk], [object_type_name] FROM [objects];

INSERT INTO [constraints] SELECT COUNT(NAME)-6 FROM PRAGMA_TABLE_INFO('users');
SELECT [pk], [enabled], [real_name], [inactivity_timeout], 
       [ui_locale], [email_addresses] FROM [users];

INSERT INTO [constraints] SELECT COUNT(NAME)-19 FROM PRAGMA_TABLE_INFO('accounts');
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
       [email_addresses],
       [fk_user] FROM [accounts];

INSERT INTO [constraints] SELECT COUNT(NAME)-3 FROM PRAGMA_TABLE_INFO('activity_types');
SELECT [pk], [name], [description] FROM [activity_types];

INSERT INTO [constraints] SELECT COUNT(NAME)-8 FROM PRAGMA_TABLE_INFO('activities');
SELECT [pk], [name], [description], [timeout],
       [require_comment_on_start], [require_comment_on_finish], 
       [full_screen_reminder], [fk_activity_type] FROM [activities];

INSERT INTO [constraints] SELECT COUNT(NAME)-1 FROM PRAGMA_TABLE_INFO('public_activities');
SELECT [pk] FROM [public_activities];

INSERT INTO [constraints] SELECT COUNT(NAME)-2 FROM PRAGMA_TABLE_INFO('private_activities');
SELECT [pk], [fk_owner] FROM [private_activities];

DROP TABLE [constraints];

