<?php
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     User_operations_model                                                   */
/*                                                                             */
/*             functionality dealing with user-management and lookups          */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class User_operations_model extends CI_Model {
  
  function __construct(){
    parent::__construct();
//    define("USER_CACHE_TABLE2", 'user_cache');
    $this->load->helper('opwhse_search');
  }


  function refresh_user_info($prn){
    $DB_info = $this->load->database('default', TRUE);
    //grab user info from Ops Whse
    $user_details_array = get_name_and_prn_array_opw('prn',$prn);
    $entries = $user_details_array[$prn];
    

    $username = $entries['first_name'] != null ? $entries['first_name'] : "Anonymous Stranger";
    $fullname = $username." ".$entries['last_name'];
    
    $values = array(
        'first_name' => $entries['first_name'],
        'last_name' => $entries['last_name'],
        'display_name' => $fullname,
        'email' => $entries['mail'],
        'telephone' => $entries['telephone'],
        'updated_at' => NULL 
      );
          
    //check for prn in database
    if($this->is_user_in_database($prn)) {
      //update user_info
      $DB_info->update("user_cache",$values, array('network_id' => $prn));
//      echo $DB_info->last_query();
    }else{
      //add user_info to cache
      $values['network_id'] = $prn;
      $values['created_at'] = null;
      $DB_info->insert("user_cache",$values);
    }
    $retval = $DB_info->affected_rows() > 0 ? true : false;
    return $retval;
  }


  function get_permission_level_info($admin_access_level){
    $DB_data = $this->load->database('default',TRUE);
    $query = $DB_data->get_where("user_privilege_levels",array('privilege_level' => $admin_access_level),1);
    if($query && $query->num_rows()>0){
      $desc = $query->row()->privilege_name;
    }else{
      $desc = 'Guest';
    }
    return $desc;
  }
  
  
  
  function get_user_permissions_level($group_list){
    $DB_info = $this->load->database('ws_info',TRUE);
    if(!$group_list || !is_array($group_list)){
      $group_list = array();
    }
    $query = $DB_info->select(array('privilege_level','group_list'))->get('user_privilege_levels');
    $max_level = 100;
    if($query && $query->num_rows()>0){
      $levels = array();
      foreach($query->result() as $row){
        $levels[$row->privilege_level] = array_intersect($group_list,explode(',',$row->group_list));
      }
      $levels = array_filter($levels);
      krsort($levels);
      foreach($levels as $level => $list){
        $max_level = $level > $max_level ? $level : $max_level;
        continue;
      }
    }
    return $max_level;
  }
 
   function is_user_in_database($prn){
    //look for user
    $DB_info = $this->load->database('default',true);
    $query = $DB_info->where('network_id', $prn)->from("user_cache");
    $retval = $DB_info->count_all_results() > 0 ? true : false;      
    return $retval;
  }
  
  function is_user_update_required($last_observed_timestamp){
    $stored_timestamp = strtotime($last_observed_timestamp);
    $now = time();
    $term = 24 * 60 * 60; //24 hours
    $diff = $now - $stored_timestamp;
    
    $response = $diff >= $term ? true : false;
     
    return $response;
  }
  
  function get_user_assignment_picklist(){
    $DB_data = $this->load->database('default',TRUE);
    $DB_data->order_by('display_name');
    $query = $DB_data->select(array('display_name','telephone','network_id'))->get_where('user_cache',array('is_staff' => 1));
    $results = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        $results[$row->network_id] = "{$row->display_name} - Phone: {$row->telephone}";
      }
    }
    array_unshift($results, " Select a staff member...");
    return $results;
  }
  

}
