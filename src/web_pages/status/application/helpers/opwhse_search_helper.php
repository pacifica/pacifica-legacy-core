<?php 
if(!defined('BASEPATH'))
  exit('No direct script access allowed');

function get_user_details_opw( $user_id ){
  $results = get_name_and_prn_array_opw('prn',$user_id);
  return $results[$user_id];
}

function get_name_and_prn_list( $search_type, $query, $additional_fields_array = false ){
  return json_encode(get_name_and_prn_array_opw($search_type,$query));
}

function get_name_and_prn_array_opw($search_type,$query){
  $CI =& get_instance();
  $valid_search_types = array(
    'prn'=>'network_id',
    'name'=>'last_name',
    'email'=>'internet_mail_address'
  );
  
  if(array_key_exists($search_type,$valid_search_types)){
    $search_type = $valid_search_types[$search_type];
  }else{
    $retval = array(
      "entries" => null,
      "error" => "'$search_type' is not a valid search type"
    );
    return $retval;
  }
  
  $employee_table = "vw_pub_bmi_employee";
  $rbac_table =  "vw_pub_rbac_role_all_members";
  $department_table = "vw_pub_bmi_department";
  
  $DB_opwhse = $CI->load->database('opwhse', TRUE);
  
  //get main user details
  $select_array = array(
    "lower(e.network_id) as prn", "lower(e.network_id) as id", "COALESCE(e.pref_first_name,e.first_name,'') as first_name",
    "COALESCE(e.pref_middle_init,e.middle_initial,'') as middle_initial", "COALESCE(e.pref_last_name,e.last_name,'') as last_name",
    "e.business_title as title", "d.desc30 as department", "COALESCE(e.primary_work_phone,e.contact_work_phone,'') as telephone",
    "e.internet_email_address as mail"
  );
  
 // var_dump($valid_search_types); 
//  echo $search_type;
  $DB_opwhse->select($select_array);
  $DB_opwhse->like(array($search_type => $query));
  $DB_opwhse->join("{$department_table} d","d.org_struc_id = e.reporting_org_id");
  $query = $DB_opwhse->get("{$employee_table} e");
  $retval = array();
  $emplid_lookup = array();
  if($query && $query->num_rows()>0){
    foreach($query->result_array() as $row){
      $row['id'] = strtolower($row['id']);
//      $row['prn'] = strtolower($row['prn']);
      $row['mail'] = strtolower($row['mail']);
      $emplid_lookup[strval($row['prn'])] = $row['id'];
//      var_dump($row);
      unset($row['prn']);
      $retval[strtolower(strval($row['id']))] = $row;
      $retval[strtolower(strval($row['id']))]['group_list'] = "";
    }
  }
     
  $group_select = array('m.parent_role_name as group_name','lower(e.network_id) as prn');
  
  $DB_opwhse->select($group_select)->order_by('m.emplid');
  $DB_opwhse->like('m.parent_role_name','magres');
  $DB_opwhse->join("{$employee_table} e","m.emplid = e.emplid");
  $groups_query = $DB_opwhse->where_in('e.network_id',$emplid_lookup)->get("{$rbac_table} m");
//  echo $DB_opwhse->last_query();
  if($groups_query && $groups_query->num_rows()>0){
    foreach($groups_query->result_array() as $group_row){
      $retval[$emplid_lookup[$group_row['prn']]]['group_list'][] = $group_row['group_name'];
    }
  }else{
    //$retval[$emplid_lookup[$retval['id']]]['group_list'][] = "";
  }
  return $retval;
}

//function get_name_and_prn_array_old( $search_type, $query, $additional_fields_array = false ){
//  $CI = &get_instance();
//  $error_list = array(
//  );
//  $query = trim($query,'.');  
//  if(!isset($krb5ccname)){
//    $krb5ccname = isset($_SERVER['KRB5CCNAME']) ? $_SERVER['KRB5CCNAME'] : false;
//  }  
//  $valid_search_types = array(
//    'prn'=>'samaccountname',
//    'name'=>'cn',
//    'email'=>'mail'
//  );  
//  if(array_key_exists($search_type,$valid_search_types)){
//    $search_type = $valid_search_types[$search_type];
//  }else{
//    $retval = array(
//      'entries'=>null,
//      'error'=>'\'$search_type\' is not a valid search type'
//    );
//    return $retval;
//  }  
//  $ldap_server_address = $CI->config->item('ldap_server_address');
//  $ldapconn = ldap_connect($ldap_server_address);  
//  if(!$ldapconn){
//    $retval = array(
//      'entries'=>null,
//      'error'=>'Could Not Connect to LDAP Server'
//    );
//    return $retval;
//  }  
//  $r = ldap_set_option(NULL,LDAP_OPT_PROTOCOL_VERSION,3);  
//  if($krb5ccname && strlen($krb5ccname) > 0){
//    //echo "GSS-API Binding";
//    putenv("KRB5CCNAME=".$krb5ccname) or die('no cached tix');
//    $ldapbind = ldap_sasl_bind($ldapconn,NULL,NULL,"GSSAPI");
//  }else{
//    //echo "Simple Binding";
//    $ldaprdn = $CI->config->item('ldap_svc_account');
//    $ldappass = $CI->config->item('ldap_creds');
//    $ldapbind = ldap_bind($ldapconn,$ldaprdn,$ldappass);
//  }
//  if($ldapbind){
//    $dn = 'OU=Managed Users,dc=PNL,dc=GOV';
//    //$filter="(&(objectclass=person)(|(samaccountname=".$query."*)(cn=*".$query."*)))";
//    $search_string = $search_type != 'mail' ? "({$search_type}=*{$query}*)" : "(|({$search_type}=*{$query}*)(proxyAddresses=*:*{$query}*))";
//    $filter = "(&(objectclass=person){$search_string})";
//    //echo "filter = ".$filter;
//    $justthese = array(
//      'samaccountname',
//      'cn',
//      'sn',
//      'givenname',
//      'initials',
//      'mail',
//      'title'
//    );
//    if(is_array($additional_fields_array)){
//      $justthese = array_merge($justthese,$additional_fields_array);
//    }
//    //var_dump($justthese);
//    $sr = ldap_search($ldapconn,$dn,$filter);
//    ldap_sort($ldapconn,$sr,'cn');
//    $entries = ldap_get_entries($ldapconn,$sr);
//    unset($entries['count']);
//    $clean_entries = array(
//    );
//    foreach ($entries as $index=>$record){
//      $clean_entry = _cleanUpEntry($record);
//      //        echo "cleaned_entries\n";
//      //        var_dump($clean_entry);
//      $temp_entry = array(
//      );
//      $prn = isset($clean_entry['samaccountname']) ? strtolower($clean_entry['samaccountname']) : false;
//      $name = isset($clean_entry['cn']) ? $clean_entry['cn'] : false;
//      $fn = isset($clean_entry['givenname']) ? $clean_entry['givenname'] : false;
//      $mi = isset($clean_entry['initials']) ? $clean_entry['initials'] : false;
//      $ln = isset($clean_entry['sn']) ? $clean_entry['sn'] : false;
//      $title = isset($clean_entry['title']) ? $clean_entry['title'] : false;
//      $dept = isset($clean_entry['department']) ? $clean_entry['department'] : false;
//      $phone = isset($clean_entry['telephonenumber']) ? $clean_entry['telephonenumber'] : false;
//      $mail = isset($clean_entry['mail']) ? $clean_entry['mail'] : false;
//      //        $hid = isset($clean_entry['extensionattribute1']) ? strtolower($clean_entry['extensionattribute1']) : false;
//      $hid_matcher = "/\w=\w(\w+);$/i";
//      if(isset($clean_entry['textencodedoraddress'])){
//        preg_match($hid_matcher,$clean_entry['textencodedoraddress'],$matches);
//        $hid = strtolower($matches[1]);
//      }else{
//        $hid = $prn;
//      }
//      $proxy_addresses = isset($clean_entry['proxyaddresses']) ? extract_alternate_email_addresses($clean_entry['proxyaddresses']) : false;
//      if(!$prn)
//        die("no prn");
//      if($prn){
//        $temp_entry['id'] = $prn;
//      }
//      //if($name) {$temp_entry['display_name'] = $name;}
//      if($fn){
//        $temp_entry['first_name'] = $fn;
//      }
//      if($mi){
//        $temp_entry['middle_initial'] = $mi;
//      }
//      if($ln){
//        $temp_entry['last_name'] = $ln;
//      }
//      if($title){
//        $temp_entry['title'] = $title;
//      }
//      if($dept){
//        $temp_entry['department'] = $dept;
//      }
//      if($phone){
//        $temp_entry['telephone'] = $phone;
//      }
//      if($mail){
//        $temp_entry['mail'] = strtolower($mail);
//      }
//      if($hid){
//        $temp_entry['hid'] = $hid;
//      }
//      if($proxy_addresses){
//        $temp_entry['alternate_addresses'] = $proxy_addresses;
//      }      
//      if($additional_fields_array){
//        foreach ($additional_fields_array as $index=>$attribute){
//          $value = isset($clean_entry[$attribute]) ? $clean_entry[$attribute] : false;
//          if($value){
//            $temp_entry[$attribute] = $value;
//          }
//        }
//      }      
//      if(sizeof($temp_entry) > 0){
//        $clean_entries[$prn] = $temp_entry;
//      }
//    }
//    if(sizeof($clean_entries) > 0){
//      $retval = array(
//        'results'=>$clean_entries
//      );
//    }else{
//      $retval = false;
//    }
//  }else{
//    $error = "Could not bind to LDAP Server";
//    $retval = array(
//      'results'=>null,
//      'error'=>$error
//    );
//  }
//  return $retval;
//}
//
//function _cleanUpEntry( $entry ){
//  $retEntry = array(
//  );
//  for($i = 0;$i < $entry['count'];$i++){
//    $attribute = $entry[$i];
//    if($entry[$attribute]['count'] == 1){
//      $retEntry[$attribute] = $entry[$attribute][0];
//    }else{
//      for($j = 0;$j < $entry[$attribute]['count'];$j++){
//        $retEntry[$attribute][] = $entry[$attribute][$j];
//      }
//    }
//  }
//  return $retEntry;
//}

//function _array_insert( $arr, $ins ){
//  # Loop through all Elements in $ins:
//  if(is_array($arr) && is_array($ins))
//    foreach ($ins as $k=>$v){
//      # Key exists in $arr and both Elemente are Arrays: Merge recursively.
//      if(isset($arr[$k]) && is_array($v) && is_array($arr[$k]))
//        $arr[$k] = _array_insert($arr[$k],$v);
//      # Place more Conditions here (see below)
//      # ...
//      # Otherwise replace Element in $arr with Element in $ins:
//      else
//        $arr[$k] = $v;
//    }
//  # Return merged Arrays:
//  return ($arr);
//}
//
//function extract_alternate_email_addresses( $proxy_address_list ){
//  $ret_list = array(
//  );
//  $match_pattern = "/^smtp:(\b[\w._%+-]+@(?:[\w-]+\.)[\w]{2,4}\b)$/i";
//  foreach ($proxy_address_list as $address){
//    if(preg_match($match_pattern,$address,$matches)){
//      $ret_list[] = strtolower($matches[1]);
//    }
//  }
//  return $ret_list;
//}

