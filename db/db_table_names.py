
###################
# structure rules #
###################
# Name of DB table -> dict{list[]}, then in list:
# 0. Names of columns with table name -> list[name of table with _ at the and then name of column]
# 1. original names of columns in table -> list[column names]
# 2. data type -> list[int, str or float]
# 3. primary and required keys -> list[names of columns]
# 4. sequences, usually one or empty -> dict{seq name} 
# 5. parent table, usually one or empty -> dict{name of parent table: dict{'name of parent table column : name of current table where should the value go}}
#    E.g. parent Table: {<parentTable> : {'<NameOfParentColumnFromWhereValueNeedsToCome>' : '<currentTableAndTheColumnNameWhereValueNeedsToBeInserted>' }}
# 6. Usually empty, but if the table has seq which is primary key, 
#    then for update is needed another field which is saved here -> list
# 7. Usually empty, but some tables get update or insert over REST-API. -> dict{call data} and list[tables which are connected or alone]
#####################################

db_tables = {
    'person' : [
        [
            'person_id',
            'person_firstname',
            'person_lastname',
            'person_age'
            
        ], # With table names
        [
            'id',
            'firstname',
            'lastname',
            'age'
        ], # original names
        [
            0,
            '',
            '',
            0
        ], # types
        [
            'id'
        ], # primary keys
        {}, # seq
        {}, # parent table
        [], # if seq, then are here fields/columns for search
        {}
    ],
    'family' : [
        [   
            'family_id',
            'family_status',
            'family_children'
        ],
        [
            'id',
            'status',
            'children'
        ],
        [
            0,
            '',
            0
        ],
        [   
            'id' 
        ],
        {},
        {
            'person' : {
                'id' : 'id'
            }
        },
        [],
        {}
    ],
    'email' : [
        [   
            'email_id',
            'email_email'
        ],
        [
            'id',
            'email'
        ],
        [
            0,
            ''
        ],
        [   
            'id' 
        ],
        {},
        {
            'person' : {
                'id' : 'id'
            }
        },
        [],
        {}
    ],
    'job' : [
        [
            'job_id',
            'job_position',
            'job_company'
        ],
        [
            'id',
            'position',
            'company'
        ],
        [
            0,
            '',
            ''
        ],
        [
            'id'
        ],
        {},
        {
            'person' : {
                'id' : 'id'
            }
        },
        [],
        {
            'rest-api' : {
                'loginUrl' : 'some url',
                'loginUsername' : 'some username',
                'loginPassword' : 'some password',
                'url' : 'some url',
                'headerLogin' : {
                    'some header': 'some header'
                    },
                'header' : {
                    'some header': 'some header'
                },
                'special' : 'id'
            },
            'job' : ['all'], # 'all' means all columns/fields otherwise what is written.
            'family' : ['status']
        }
    ],
    'user' : [
        [   
            'user_id',
            'user_user',
            'user_usergroup',
            'user_password'
        ],
        [
            'id',
            'user',
            'usergroup',
            'password'
        ],
        [
            0,
            '',
            '',
            ''
        ],
        [   
            'id',
            'user'
        ], 
        {
            'user_id' : 'user_id_seq.nextval'
        },
        {},
        [
            'user'
        ],
        {}
    ],
    'userlogin' : [
        [
            'userlogin_user',
            'userlogin_userlogin'
        ],
        [
            'user',
            'userlogin'
        ],
        [
            '',
            ''
        ],
        [
            'user'
        ],
        {},
        {
            'user' : {
                'user' : 'user'
            }
        },
        [],
        {}
    ]
}