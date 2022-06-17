
# originally from the App/DB

prop = {
    'csvSeperator' : ';',
    'testRun' : 'J',
    'notInitDBvalues' : '',
    'childTables' : 'family,email,job,userlogin',
    'csvContent' : 'id;firstname;lastname;age;status;children;email;position;company', # used the same as renamed, usually it is differnt.
    'db_tables' : 'person,family,email,job,user,userlogin',
    'dictReader' : 'J',
    'ifValueInAttrThenValue' : '',
    'ignoreFieldValid' : '',
    'modifyAttrValueWithOtherAttrValues' : 'user_id?=person_id!=user_user?=person_firstname?+person_lastname!=user_usergroup?=admin!=user_password?=person_firstname?^upper?+1234!=userlogin_userlogin?=user_user!=',
    'renamedCsvContent' : 'person_id;person_firstname;person_lastname;person_age;family_status;family_children;email_email;job_position;job_company', # Table and column name from DB.
    'whoFirstModify' : ''
}


