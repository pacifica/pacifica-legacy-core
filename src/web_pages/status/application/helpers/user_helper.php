<?php 
if(!defined('BASEPATH'))
  exit('No direct script access allowed');  
// --------------------------------------------------------------------

function get_user(){
  $user = '(unknown)';
  if(isset($_SERVER["REMOTE_USER"])){
    $user = str_replace('@PNL.GOV','',$_SERVER["REMOTE_USER"]);
  }
  return strtolower($user);
}

function get_user_details($user_id){
  $user_info = array(
    'user_id' => strtolower($_SERVER['REMOTE_USER']),
    'first_name' => $_SERVER['LDAP_GIVENNAME'],
    'middle_initial' => $_SERVER['LDAP_INITIALS'],
    'last_name' => $_SERVER['LDAP_SN'],
    'email' => strtolower($_SERVER['LDAP_MAIL'])    
  );
  return $user_info;
}
