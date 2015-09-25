<?php
require_once APPPATH.'libraries/Requests.php';
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     Myemsl_model                                                            */
/*                                                                             */
/*             functionality dealing with MyEMSL API Access calls, etc.        */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class API_model extends CI_Model {
  
  function __construct(){
    parent::__construct();
    $this->load->helper('myemsl');
    Requests::register_autoloader();
    $this->myemsl_ini = read_myemsl_config_file('general');
    $this->load->database('default');
  }
  
  function get_available_group_types($filter = ""){
    if(!empty($filter)){
      $this->db->like('type',$filter);
    }
    $results = array();
    $query = $this->db->select('type')->distinct()->order_by('type')->get('groups');
    if($query && $query->num_rows()>0){
      foreach($query->result() as $row){
        $results[] = $row->type;
      }
    }
    return $results;
  }

  function search_by_metadata($metadata_pairs, $search_operator = "AND"){
    // check for valid search operator
    $search_operator = strtoupper($search_operator);
    $valid_operators = array('AND','OR');
    if(!in_array($search_operator,$valid_operators)){
      $search_operator = "AND";
    }
    
    
    //check for valid types
    $clean_pairs = $this->clean_up_metadata_pairs($metadata_pairs);
    $compiled_info = array('results_count' => 0);
    if(empty($clean_pairs)){
      return $compiled_info;
    }
    
    //build the search query for group_id list
    $found_group_ids = array();
    $group_id_relationships = array();
    foreach($clean_pairs as $field => $value){
      if(!array_key_exists($field,$group_id_relationships)){
        $group_id_relationships[$field] = array();
      }
      $where_array = array(
        'lower(type)' => strtolower($field), 'lower(name)' => !is_numeric($value) ? strtolower($value) : $value
      );
      $this->db->select('group_id')->where($where_array);
      $group_query = $this->db->get('groups',1);
      if($group_query && $group_query->num_rows() > 0){
        foreach($group_query->result() as $group_row){
          $group_id_relationships[$field][] = $group_row->group_id;
          $found_group_ids[] = $group_row->group_id;
        }
      }
    }
    
    
    
    //now use the group_ids to find the items related to each one
    if(!empty($found_group_ids)){
      $item_results = array();
      $item_query = $this->db->where_in('group_id', $found_group_ids)->get('group_items');
      if($item_query && $item_query->num_rows()>0){
        foreach($item_query->result() as $item_row){
          if(!array_key_exists($item_row->group_id,$item_results)){
            $item_results[$item_row->group_id] = array('items' => array());
          }
          
          $item_results[$item_row->group_id]['items'][] = $item_row->item_id;
        }
        
        $item_list = array_shift($item_results);
        $item_list = $item_list['items'];
        if($search_operator == "AND"){
          foreach($item_results as $filter){
            $item_list = array_merge($item_list,$filter['items']);
          }
        }else{
          foreach($item_results as $filter){
            $item_list = array_intersect($item_list, $filter['items']);
          }
        }
        $file_info = $this->get_transaction_info($item_list);
        $compiled_info = $this->get_metadata_entries($file_info);
      }
    }
    return $compiled_info;
    
    //now that we have a list of items shared amongst the selection criteria
    // let's get the info for all of them
  }

  function get_item_info($item_id){
    $select_array = array(
      'files.item_id as itemid', "CONCAT(files.subdir,'/',files.name) as full_path",
      'files.name as filename', 'files.size', "transactions.stime AT TIME ZONE 'US/Pacific' as stime",
      'hashsums.hashsum', 'files.verified', 'files.aged'
    );
    $fi_row = array('error_message' => 'Could not find item.');
    $this->db->select($select_array)->where("files.item_id",$item_id);
    $this->db->from('files')->join('hashsums', 'files.item_id = hashsums.item_id');
    $this->db->join('transactions','transactions.transaction = files.transaction');
    $file_info_query = $this->db->limit(1)->get();
    if($file_info_query && $file_info_query->num_rows()>0){
      $fi_row = $file_info_query->row_array();
      $fi_row['type'] = 'file';
      $fi_row['checksum'] = array('sha1' => $fi_row['hashsum']);
      unset($fi_row['hashsum']);
      // $file_info = array('myemsl' => $fi_row);
    }
    
    return $fi_row;
  }


  private function get_transaction_info($item_list){
    //get a list of transactions for this list of item_id's
    $trans_query = $this->db->select('transaction')->distinct()->where_in('item_id',$item_list)->get('files');
    $transaction_list = array();
    if($trans_query && $trans_query->num_rows()>0){
      foreach($trans_query->result() as $row){
        $transaction_list[$row->transaction] = '0000-00-00 00:00:00';
      }
    }
    $file_info = array();
    if(!empty($transaction_list)){
      //first, get the submission times for each transaction
      $this->db->select(array("stime AT TIME ZONE 'US/Pacific' as stime", "transaction"));
      $stime_query = $this->db->where_in('transaction', array_keys($transaction_list))->get('transactions');
      if($stime_query && $stime_query->num_rows()>0){
        foreach($stime_query->result() as $stime_row){
          $stime = new DateTime($stime_row->stime);
          $transaction_list[$stime_row->transaction] = $stime->format('Y-m-d H:i:s');
        }
      }
     
      $select_array = array(
        'f.item_id', "CONCAT(f.subdir,'/',f.name) as full_path",
        'f.name as filename', 'f.size as size_in_bytes',
        'f.transaction', 'h.hashsum', 'f.verified', 'f.aged'
      );
      $file_info = array();
      $this->db->select($select_array)->where_in('transaction',array_keys($transaction_list));
      $this->db->from('files f')->join('hashsums h', 'f.item_id = h.item_id');
      $file_info_query = $this->db->get();
      if($file_info_query && $file_info_query->num_rows()>0){
        foreach($file_info_query->result_array() as $fi_row){
          $fi_row['submit_time'] = $transaction_list[$fi_row['transaction']];
          $file_info['transactions'][$fi_row['transaction']]['file_info'][$fi_row['item_id']] = $fi_row;
        }
      }
    }
    return $file_info;
    
  }


  private function get_metadata_entries($file_info){
    //get a representative item_id from each transaction
    $this->db->select(array('MIN(item_id) as rep_item_id','transaction'))->group_by('transaction');
    $item_query = $this->db->where_in('transaction',array_keys($file_info['transactions']))->get('files');
    if($item_query && $item_query->num_rows()>0){
      foreach($item_query->result() as $item_row){
        $this->db->where('item_id',$item_row->rep_item_id);
        $file_info['transactions'][$item_row->transaction]['result_count'] = count($file_info['transactions'][$item_row->transaction]['file_info']);
        $group_query = $this->db->from('groups g')->join('group_items gi', 'gi.group_id = g.group_id')->get();
        if($group_query && $group_query->num_rows()>0){
          foreach($group_query->result() as $md_row){
            $file_info['transactions'][$item_row->transaction]['metadata'][$md_row->type] = $md_row->name;
          }
        }
      }
    }
    return $file_info;
  }
  
  
  private function clean_up_metadata_pairs($pairs){
    //check for valid types
    $cleaned_types = array();
    $clean_pairs = array();
    $valid_types = $this->get_available_group_types();
    foreach($pairs as $field => $value){
      if(!in_array($field, $valid_types)){
        //hmmm... try stripping off group.* if it exists
        if(preg_match('/group\.(.+)/i',$field,$m)){
          $new_field = $m[1];
          if(in_array($new_field, $valid_types)){
            $cleaned_types[$field] = $new_field;
            continue;
          }
        }
      }else{
        $cleaned_types[$field] = $field;
      }
    }
    foreach($pairs as $field => $value){
      if(array_key_exists($field,$cleaned_types)){
        $clean_pairs[$cleaned_types[$field]] = $value;
      }
    }
    return $clean_pairs;
  }

}
?>