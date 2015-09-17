<?php
require_once APPPATH.'libraries/Requests.php';
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     Myemsl_model                                                            */
/*                                                                             */
/*             functionality dealing with MyEMSL API Access calls, etc.        */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class Myemsl_model extends CI_Model {
  
  function __construct(){
    parent::__construct();
    $this->load->helper('myemsl');
    Requests::register_autoloader();
    $this->myemsl_ini = read_myemsl_config_file('general');
  }
  
  
  function get_user_info(){
    $protocol = isset($_SERVER["HTTPS"]) && $_SERVER["HTTPS"] == "on" ? "https" : "http";
    $basedir = 'myemsl';
    // $url_base =  dirname(dirname($this->myemsl_ini['getuser']['prefix']));
    $url_base = "{$protocol}://localhost";
    $options = array(
      'verify' => false,
      'timeout' => 60,
      'connect_timeout' => 30
    );
    $headers = array();
    
    foreach($_COOKIE as $cookie_name => $cookie_value){
      $headers[] = "{$cookie_name}={$cookie_value}";
    }

    $headers = array('Cookie' => implode(';',$headers));
    $session = new Requests_Session($url_base, $headers, array(), $options);
    
    try{
      $response = $session->get('/myemsl/userinfo');
      $user_info = json_decode($response->body,true);
    }catch(Exception $e){
      $user_info = array('error' => 'Unable to retrieve User Information');
      return $user_info;
    }

    $DB_myemsl = $this->load->database('default',true);
    
    //go retrieve the instrument/group lookup table
    $DB_myemsl->like('type','Instrument.')->or_like('type','omics.dms.instrument');
    $query = $DB_myemsl->get('groups');
    
    $inst_group_lookup = array();
    
    if($query && $query->num_rows()>0){
      foreach($query->result() as $row){
        if($row->type == 'omics.dms.instrument'){
          $inst_id = intval($row->group_id);
        }elseif(strpos($row->type, 'Instrument.') >= 0){
          $inst_id = intval(str_replace('Instrument.','',$row->type));
        }else{
          continue;
        }
        $inst_group_lookup[$inst_id]['groups'][] = intval($row->group_id);
      }
    }
    
    $new_instruments_list = array();
    
    foreach($user_info['instruments'] as $eus_instrument_id => $inst_info){
      $new_instruments_list[$eus_instrument_id] = $inst_info;
      if(array_key_exists($eus_instrument_id, $inst_group_lookup)){
        $new_instruments_list[$eus_instrument_id]['groups'] = $inst_group_lookup[$eus_instrument_id]['groups'];
      }else{
        $new_instruments_list[$eus_instrument_id]['groups'] = array();
      }
    }
    $user_info['instruments'] = $new_instruments_list;
    
    
    return $user_info;
  }
 
  
  
}
?>