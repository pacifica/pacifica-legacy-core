<?php
if(!defined('BASEPATH'))
  exit('No direct script access allowed');

function get_user_details_myemsl($eus_id){
  $CI =& get_instance();
  
  $users_table = "UP_USERS";
  $DB_eus = $CI->load->database('eus_for_myemsl',TRUE);
  
  $select_array = array('person_id', 'first_name','last_name', 'email_address', 'network_id');
  
  $query = $DB_eus->select($select_array)->get_where($users_table, array('person_id' => $eus_id),1);
  
  if($query && $query->num_rows() > 0){
    $results = $query->row_array();
  }
  return $results;
}


function read_myemsl_config_file($file_specifier = 'general'){
  $CI =& get_instance();
  $ini_path = $CI->config->item('myemsl_config_file_path');
  $ini_items = parse_ini_file("{$ini_path}{$file_specifier}.ini", TRUE);
  return $ini_items;
}

function generate_cart_token($item_list,$eus_person_id){
  $uuid = "huYNwptYEeGzDAAmucepzw";
  $duration = 3600;
  
  //grab private key file
  $fp = fopen('/etc/myemsl/keys/item/local.key','r');
  $priv_key = fread($fp,8192);
  fclose($fp);
  $pkey_id = openssl_get_privatekey($priv_key);
  
  $s_time = new DateTime();
  $time = $s_time->format(DATE_ATOM);
  // $time = '2015-05-08T16:07:06-07:00';
  
  $token_object = array(
    'd' => $duration, 'i' => $item_list, 'p' => intval($eus_person_id),
    's' => $time, 'u' => $uuid
  );
  
  $token_json = json_encode($token_object);
  
  $trimmed_token = trim($token_json,'{}');
  
  openssl_sign($trimmed_token,$signature,$pkey_id,'sha256');
  openssl_free_key($pkey_id);
  
  $cart_token = strlen($trimmed_token).$trimmed_token.$signature;
  
  $cart_token_b64 = base64_encode($cart_token);
  
  return $cart_token_b64;
  
}

?>