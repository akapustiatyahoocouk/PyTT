CREATE TEMP TABLE [constraints]
(
    [condition] INTEGER NOT NULL CHECK([condition] = 0)
);


SELECT [pk], [object_type_name] FROM [objects];
INSERT INTO [constraints] SELECT COUNT(NAME)-2 FROM PRAGMA_TABLE_INFO('objects');
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('objects') WHERE NAME='pk' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('objects') WHERE NAME='object_type_name'AND type='VARCHAR(32)';


SELECT [pk], [enabled], [real_name], [inactivity_timeout], 
       [ui_locale], [email_addresses] FROM [users];
INSERT INTO [constraints] SELECT COUNT(NAME)-6 FROM PRAGMA_TABLE_INFO('users');
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='pk' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='enabled' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='real_name' AND type='VARCHAR(128)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='inactivity_timeout' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='ui_locale' AND type='VARCHAR(64)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('users') WHERE NAME='email_addresses' AND type='TEXT';


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
INSERT INTO [constraints] SELECT COUNT(NAME)-19 FROM PRAGMA_TABLE_INFO('accounts');
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='pk' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='enabled' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='login' AND type='VARCHAR(128)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='password_hash' AND type='CHAR(40)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='is_administrator' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_users' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_stock_items' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_beneficiaries' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_workloads' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_public_activities' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_public_tasks' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_private_activities' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_manage_private_tasks' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_log_work' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_log_events' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_generate_reports' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='can_backup_and_restore' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='email_addresses' AND type='TEXT';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('accounts') WHERE NAME='fk_user' AND type='INTEGER';


SELECT [pk], [name], [description] FROM [activity_types];
INSERT INTO [constraints] SELECT COUNT(NAME)-3 FROM PRAGMA_TABLE_INFO('activity_types');
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activity_types') WHERE NAME='pk' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activity_types') WHERE NAME='name' AND type='VARCHAR(128)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activity_types') WHERE NAME='description' AND type='TEXT';


SELECT [pk], [name], [description], [timeout],
       [require_comment_on_start], [require_comment_on_finish], 
       [full_screen_reminder], [fk_activity_type],
       [completed], [fk_owner] FROM [activities];
INSERT INTO [constraints] SELECT COUNT(NAME)-10 FROM PRAGMA_TABLE_INFO('activities');
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='pk' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='name' AND type='VARCHAR(128)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='description' AND type='TEXT';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='timeout' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='require_comment_on_start' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='require_comment_on_finish' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='full_screen_reminder' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='fk_activity_type' AND type='INTEGER';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='completed' AND type='CHAR(1)';
INSERT INTO [constraints] SELECT COUNT(*)-1 FROM PRAGMA_TABLE_INFO('activities') WHERE NAME='fk_owner' AND type='INTEGER';


DROP TABLE [constraints];

