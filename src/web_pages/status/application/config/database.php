<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');
/*
| -------------------------------------------------------------------
| DATABASE CONNECTIVITY SETTINGS
| -------------------------------------------------------------------
| This file will contain the settings needed to access your database.
|
| For complete instructions please consult the 'Database Connection'
| page of the User Guide.
|
| -------------------------------------------------------------------
| EXPLANATION OF VARIABLES
| -------------------------------------------------------------------
|
|	['hostname'] The hostname of your database server.
|	['username'] The username used to connect to the database
|	['password'] The password used to connect to the database
|	['database'] The name of the database you want to connect to
|	['dbdriver'] The database type. ie: mysql.  Currently supported:
				 mysql, mysqli, postgre, odbc, mssql, sqlite, oci8
|	['dbprefix'] You can add an optional prefix, which will be added
|				 to the table name when using the  Active Record class
|	['pconnect'] TRUE/FALSE - Whether to use a persistent connection
|	['db_debug'] TRUE/FALSE - Whether database errors should be displayed.
|	['cache_on'] TRUE/FALSE - Enables/disables query caching
|	['cachedir'] The path to the folder where cache files should be stored
|	['char_set'] The character set used in communicating with the database
|	['dbcollat'] The character collation used in communicating with the database
|				 NOTE: For MySQL and MySQLi databases, this setting is only used
| 				 as a backup if your server is running PHP < 5.2.3 or MySQL < 5.0.7
|				 (and in table creation queries made with DB Forge).
| 				 There is an incompatibility in PHP with mysql_real_escape_string() which
| 				 can make your site vulnerable to SQL injection if you are using a
| 				 multi-byte character set and are running versions lower than these.
| 				 Sites using Latin-1 or UTF-8 database character set and collation are unaffected.
|	['swap_pre'] A default table prefix that should be swapped with the dbprefix
|	['autoinit'] Whether or not to automatically initialize the database.
|	['stricton'] TRUE/FALSE - forces 'Strict Mode' connections
|							- good for ensuring strict SQL while developing
|
| The $active_group variable lets you choose which connection group to
| make active.  By default there is only one group (the 'default' group).
|
| The $active_record variables lets you determine whether or not to load
| the active record class
*/

$active_group = 'default';
$active_record = TRUE;

$myemsl_array = parse_ini_file("/etc/myemsl/general.ini", TRUE);

$db['default']['hostname'] = $myemsl_array['metadata']['host'];
$db['default']['username'] = $myemsl_array['metadata']['user'];
$db['default']['password'] = $myemsl_array['metadata']['password'];
$db['default']['database'] = $myemsl_array['metadata']['database'];
$db['default']['dbdriver'] = "postgre";
$db['default']['dbprefix'] = "myemsl.";
$db['default']['pconnect'] = TRUE;
$db['default']['db_debug'] = TRUE;
$db['default']['cache_on'] = FALSE;
$db['default']['cachedir'] = "";


$db['ws_info']['hostname'] = 'sqlite:'.APPPATH.'config/database/myemsl_status_site_info.sqlite:';
$db['ws_info']['username'] = '';
$db['ws_info']['password'] = '';
$db['ws_info']['database'] = '';
$db['ws_info']['dbdriver'] = 'pdo';
$db['ws_info']['dbprefix'] = '';
$db['ws_info']['pconnect'] = TRUE;
$db['ws_info']['db_debug'] = TRUE;
$db['ws_info']['cache_on'] = FALSE;
$db['ws_info']['cachedir'] = '';
$db['ws_info']['char_set'] = 'utf8';
$db['ws_info']['dbcollat'] = 'utf8_general_ci';
$db['ws_info']['swap_pre'] = '';
$db['ws_info']['autoinit'] = TRUE;
$db['ws_info']['stricton'] = FALSE;


// $db['default']['hostname'] = "localhost";
// $db['default']['username'] = "myemsl_reader";
// $db['default']['password'] = "myemsl4fun";
// $db['default']['database'] = "myemsl_status_site_info";
// $db['default']['dbdriver'] = "mysql";
// $db['default']['dbprefix'] = "";
// $db['default']['pconnect'] = TRUE;
// $db['default']['db_debug'] = TRUE;
// $db['default']['cache_on'] = FALSE;
// $db['default']['cachedir'] = "";

$db['eus_for_myemsl']['hostname'] = "eusi.emsl.pnl.gov";
$db['eus_for_myemsl']['username'] = "myemsl";
$db['eus_for_myemsl']['password'] = "Gr7vakon";
$db['eus_for_myemsl']['database'] = "ERSUP";
$db['eus_for_myemsl']['dbdriver'] = "mysql";
$db['eus_for_myemsl']['dbprefix'] = "";
$db['eus_for_myemsl']['pconnect'] = TRUE;
$db['eus_for_myemsl']['db_debug'] = TRUE;
$db['eus_for_myemsl']['cache_on'] = FALSE;
$db['eus_for_myemsl']['cachedir'] = "";

$db['ers']['hostname'] = "eusi.emsl.pnl.gov";
$db['ers']['username'] = "auberry_user";
$db['ers']['password'] = "l0Ve2getEUSd3ta";
$db['ers']['database'] = "Auberry";
$db['ers']['dbdriver'] = "mysql";
$db['ers']['dbprefix'] = "";
$db['ers']['active_r'] = TRUE;
$db['ers']['pconnect'] = FALSE;
$db['ers']['db_debug'] = FALSE;
$db['ers']['cache_on'] = FALSE;
$db['ers']['cachedir'] = "";


/* End of file database.php */
/* Location: ./application/config/database.php */