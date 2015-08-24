<?php
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     Status Model                                                            */
/*                                                                             */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class Status_model extends CI_Model {
  function __construct(){
    parent::__construct();
    $this->local_timezone = "US/Pacific";
    $this->load->model('eus_model','eus');  
    $this->status_list = array(
      0 => 'Submitted', 1 => 'Received', 2 => 'Processing',
      3 => 'Verified', 4 => 'Stored', 5 => 'Available', 6 => 'Archived'
    );
  }
  
  
  /*
   * gathers wide overview data about many types of instruments for upper-level mgmt
   * 
   */
  function get_status_overview($class_filter = "", $instrument_filter = ""){
    
  }
  
  
  

  
  function get_status_for_instrument_over_range($instrument_list, $time_period = "1 day"){
    $current_time_obj = new DateTime();
    $current_time_obj->setTime($current_time_obj->getHours(),0,0);
    $start_time = date_modify($current_time_obj, "-{$time_period}");
    return $this->get_status_for_instrument_before_date($instrument_list, $start_time);
    
  }
  
  
  

  
  function get_instrument_group_list($inst_id_filter = ""){
    $DB_myemsl = $this->load->database('default',TRUE);
    
    $DB_myemsl->select(array('group_id','name','type'));
    if(!empty($inst_id_filter) && intval($inst_id_filter) >= 0){
      $where_clause = "(type = 'omics.dms.instrument' or type ilike 'instrument.%') and name not in ('foo') and (group_id = '{$inst_id_filter}' or type like 'Instrument.{$inst_id_filter}')";
    }else{
      $where_clause = "(type = 'omics.dms.instrument' or type ilike 'instrument.%') and name not in ('foo')";
    }
    
    $DB_myemsl->where($where_clause);
    $query = $DB_myemsl->order_by('name')->get('groups');
    $results_by_group = array();
    $results_by_inst_id = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        if($row->type == 'omics.dms.instrument'){
          $inst_id = intval($row->group_id);
        }elseif(strpos($row->type, 'Instrument.') >= 0){
          $inst_id = intval(str_replace('Instrument.','',$row->type));
        }else{
          continue;
        }
        $results_by_inst_id[$inst_id][$row->group_id] = $row->name;
      }
    }
    $results = array('by_group' => $results_by_group, 'by_inst_id' => $results_by_inst_id);
    return $results;
  }
  
  
  function get_proposal_group_list($proposal_id = ""){
    $DB_myemsl = $this->load->database('default',TRUE);
    
    $DB_myemsl->select(array('group_id','name','type'));
    if(!empty($proposal_id)){
      $where_clause = "(type = 'proposal') and name not in ('foo') and (group_id = '{$proposal_id}')";
    }else{
      $where_clause = "(type = 'proposal') and name not in ('foo')";
    }
    
    $DB_myemsl->where($where_clause);
    $query = $DB_myemsl->order_by('name')->get('groups');
    echo $DB_myemsl->last_query();
    $results_by_group = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        $found_proposal_id = $row->name;
        $results_by_group[$row->group_id] = $found_proposal_id;
      }
    }
    $results = array('by_group' => $results_by_group);
    // var_dump($results);
    return $results;
  }
  
  
  function get_files_for_transaction($transaction_id){
    $DB_myemsl = $this->load->database('default',TRUE);
    
    $file_select_array = array(
      'f.item_id','f.name','f.subdir',"t.stime AT TIME ZONE 'US/Pacific' as stime",'f.transaction','f.size'
    );
    
    $DB_myemsl->trans_start();
    $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");
    // echo $DB_myemsl->last_query();
    $DB_myemsl->select($file_select_array)->from('transactions t')->join('files f', 't.transaction = f.transaction');
    $DB_myemsl->where('f.transaction',$transaction_id);
    $DB_myemsl->order_by('f.subdir, f.name');
    $files_query = $DB_myemsl->get();
    $DB_myemsl->trans_complete();
    $files_list = array();
    
    if($files_query && $files_query->num_rows()>0){
      foreach($files_query->result_array() as $row){
        $files_list[$row['item_id']] = $row;
      }
      $file_tree = array();
      
      
      $dirs = array();
      foreach($files_list as $item_id => $item_info){
        $subdir = $item_info['subdir'];
        $filename = $item_info['name'];
        $path = !empty($subdir) ? "{$subdir}/{$filename}" : $filename;
        $path_array = explode('/',$path);
        build_folder_structure($dirs, $path_array, $item_info);
      }
      
      return array('treelist' => $dirs, 'files' => $files_list);
    }
  }


  function get_latest_transactions($group_id_list, $proposal_id, $last_id){
    //if last_id is -1, grab the last transaction so we can display its date as a pointer 
    $transaction_list = array();
    $DB_myemsl = $this->load->database('default',TRUE);
    $select_array = array(
      'max(f.transaction) as transaction_id',
      'max(gi.group_id) as group_id'
    );
    if(!is_array($group_id_list)){
      $group_id_list = array($group_id_list);
    }
    
    $DB_myemsl->select('group_id')->where('type','proposal')->where('name',$proposal_id);
    $prop_query = $DB_myemsl->get('groups',1);
    $proposal_group_id = $prop_query && $prop_query->num_rows() > 0 ? $prop_query->row()->group_id : -1;
    
    
    $raw_transaction_list = array();
    $DB_myemsl->trans_start();
    $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");    
    $DB_myemsl->select($select_array)->from('group_items gi')->join('files f', 'gi.item_id = f.item_id');
    $DB_myemsl->group_by('f.transaction')->order_by('f.transaction desc');
    $DB_myemsl->where_in('gi.group_id',$group_id_list);
    $DB_myemsl->where('gi.group_id',$proposal_group_id);
    $DB_myemsl->order_by('f.transaction desc');
    if($last_id > 0){
      $DB_myemsl->where_in('gi.group_id',$group_id_list)->where('f.transaction >',$last_id);
    }else{
      $DB_myemsl->limit(1);
    }
    $query = $DB_myemsl->get();
    $DB_myemsl->trans_complete();
// echo "transactions by group filtered by id\n";
// echo $DB_myemsl->last_query();
    if($query && $query->num_rows() > 0){
      //must have some new transactions
      foreach($query->result() as $row){
        $raw_transaction_list[] = intval($row->transaction_id);
      }
    }

    sort($raw_transaction_list);
    return $raw_transaction_list;
  }

  
  function get_transactions_for_group($group_id, $num_days_back, $eus_proposal_id){
    $transaction_list = array();
    $is_empty = false;
    $DB_myemsl = $this->load->database('default',TRUE);
    $results = array();
    $message = "";
    $raw_transaction_list = array();
    
    $eligible_tx_list = array();
    
    if(!empty($eus_proposal_id)){
      //get proposal group id
      $DB_myemsl->select('group_id')->where('type','proposal')->where('name',$eus_proposal_id);
      $prop_query = $DB_myemsl->get('groups',1);
      $proposal_group_id = $prop_query && $prop_query->num_rows() > 0 ? $prop_query->row()->group_id : -1;
      
      //go grab the list of eligible tx_id's
      $DB_myemsl->select('max(f.transaction) as transaction_id');
      $DB_myemsl->from('group_items gi')->join('files f', 'gi.item_id = f.item_id');
      $DB_myemsl->group_by('f.transaction')->order_by('f.transaction desc');
      $query = $DB_myemsl->where('gi.group_id',$proposal_group_id)->get();
  // echo "transaction_ids\n";
  // echo $DB_myemsl->last_query();
  // echo "\n";
      if($query && $query->num_rows() > 0){
        foreach($query->result() as $row){
          $eligible_tx_list[] = $row->transaction_id;
        }
      }
      
    }else{
      $message = "Select an EUS Proposal and Instrument to load data";
      return array('transaction_list' => $results, 'time_period_empty' => $is_empty, 'message' => $message);
    }
    
    $select_array = array(
      'max(f.transaction) as transaction_id',
      'max(gi.group_id) as group_id'
    );
    $DB_myemsl->trans_start();
    $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");    
    $DB_myemsl->select($select_array)->from('group_items gi')->join('files f', 'gi.item_id = f.item_id');
    $DB_myemsl->group_by('f.transaction')->order_by('f.transaction desc');
    if($group_id && $group_id != 0){
      if(is_array($group_id)){
        $DB_myemsl->where_in('gi.group_id',$group_id);
      }else{
        $DB_myemsl->where('gi.group_id',$group_id);
      }
    }
    if(!empty($eligible_tx_list)){
      $DB_myemsl->where_in('f.transaction', $eligible_tx_list);
      $query = $DB_myemsl->get();
    }
  // echo "get transactions by date\n";
  // echo $DB_myemsl->last_query();
  // echo "\n";
    $DB_myemsl->trans_complete();
    //filter the transactions for date
    if($query && $query->num_rows()>0){
      foreach($query->result() as $row){
        $raw_transaction_list[] = $row->transaction_id;
      }
      $today = new DateTime();
      $earliest_date = clone $today;
      $earliest_date->modify("-{$num_days_back} days");
      $DB_myemsl->trans_start();
      $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");
      $DB_myemsl->select('transaction')->where_in('transaction',$raw_transaction_list)->where("stime AT TIME ZONE 'US/Pacific' >=",$earliest_date->format('Y-m-d'));
      $trans_query = $DB_myemsl->get('transactions');
    // echo "transactions filtered by tx list";
    // echo $DB_myemsl->last_query();
    // echo "\n";      
      $DB_myemsl->trans_complete();
      if($trans_query && $trans_query->num_rows()>0){
        foreach($trans_query->result() as $row){
          $transaction_list[] = $row->transaction;
        }
      }
      if(empty($transaction_list)){
        $DB_myemsl->select('transaction')->where_in('transaction',$raw_transaction_list)->order_by('transaction desc')->limit(3);
        $trans_query = $DB_myemsl->get('transactions');
    // echo "backup Query";
    // echo $DB_myemsl->last_query();
    // echo "\n";        
        if($trans_query && $trans_query->num_rows()>0){
          foreach($trans_query->result() as $row){
            $transaction_list[] = $row->transaction;
          }
        }
        $is_empty = true;
        $list_size = $trans_query->num_rows();
        $message = "No uploads were found during this time period.<br />The {$list_size} most recent entries for this instrument are below.";
      }
      $results = $this->get_formatted_object_for_transactions($transaction_list);
      // var_dump($results);
      $group_list = $this->get_groups_for_transaction($transaction_list,false);
      foreach($group_list['groups'] as $tx_id => $group_info){
        $results['transactions'][$tx_id]['groups'] = $group_info;
        // var_dump($results['transactions'][$tx_id]['groups']);
      }
    }
    return array('transaction_list' => $results, 'time_period_empty' => $is_empty, 'message' => $message);
  }

  function get_total_size_for_transactions($transaction_id_list){
    if(!is_array($transaction_id_list)){
      $transaction_id_list = explode(',',$transaction_id_list);
    }
    $DB_myemsl = $this->load->database('default',TRUE);
    $select_array = array('transaction as id', 'sum(size) as total_size');
    $DB_myemsl->select($select_array)->group_by('transaction')->order_by('transaction');
    $results = array();
    
    if(!empty($transaction_id_list)){
      $query = $DB_myemsl->where_in('transaction',$transaction_id_list)->get('files');
      if($query && $query->num_rows()>0){
        foreach($query->result() as $row){
          $results[$row->id] = $row->total_size;
        }
      }
    }
    
    return $results;
  }

  function get_groups_for_transaction($transaction_id_list){
    $DB_myemsl = $this->load->database('default',TRUE);
    
    $select_array = array(
      'g.group_id as group_id', 'g.name as group_name',
      'g.type as group_type', 'f.transaction as tx_id'
    );
    
    $DB_myemsl->select($select_array)->distinct();
    $DB_myemsl->from('files f')->join('group_items gi', 'gi.item_id = f.item_id');
    $DB_myemsl->join('groups g', 'g.group_id = gi.group_id')->order_by('g.name');
    $query = $DB_myemsl->where_in('f.transaction', $transaction_id_list)->get();
        // echo $DB_myemsl->last_query();
    
    $inst_group_pattern = '/Instrument\.(\d+)/i';
    if($query && $query->num_rows()>0){
      $groups = array();
      foreach($query->result() as $row){
        if(preg_match($inst_group_pattern, $row->group_type, $inst_matches)){
          $groups[$row->tx_id]['instrument_id'] = "{$inst_matches[1]} [MyEMSL Group: {$row->group_id}]";
          $groups[$row->tx_id]['instrument_name'] = !empty($row->group_name) ? "{$row->group_name}" : "[Not Specified]";
        }elseif($row->group_type == 'proposal'){
          $groups[$row->tx_id]['proposal_id'] = $row->group_name;
          // if($groups['proposal_id'] != )
          $groups[$row->tx_id]['proposal_name'] = $this->eus->get_proposal_name($row->group_name);  
        }else{
          $groups[$row->tx_id][$row->group_type] = !empty($row->group_name) ? $row->group_name : "[Not Specified]";
        }
      }
      $return_set['groups'] = $groups;
    }
    return $return_set;
  }
  

  function get_formatted_object_for_job($job_id){
    $status = $this->get_job_status(array($job_id), $this->status_list);
    if(array_key_exists($job_id, $status)){
      $status = $status[$job_id];
    }else{
      return array();
    }
    $time_now = new DateTime();
    $time_string = $time_now->format('Y-m-d H:i:s');
    $job_id = strval($job_id);
    $results = array(
      'transactions' => array(
        $job_id => array(
          'status' => array(
            $job_id => array(
              $status['state'] => array(
                'jobid' => $job_id,
                'trans_id' => false,
                'person_id' => $status['person_id'],
                'step' => $status['state'],
                'message' => $this->status_list[$status['state']],
                'status' => "SUCCESS"
              )
            )
          )
        )
      ), 
      'times' => array(
        $time_string => $job_id
      )
    );
    return $results;
  }

/*
array(2) {
  ["transactions"]=>
  array(1) {
    [1387]=>
    array(1) {
      ["status"]=>
      array(1) {
        [1387]=>
        array(1) {
          [5]=>
          array(6) {
            ["jobid"]=>
            string(7) "2001387"
            ["trans_id"]=>
            string(4) "1387"
            ["person_id"]=>
            string(5) "37612"
            ["step"]=>
            string(1) "5"
            ["message"]=>
            string(9) "completed"
            ["status"]=>
            string(7) "SUCCESS"
          }
        }
      }
    }
  }
  ["times"]=>
  array(1) {
    ["2015-06-25 10:09:24"]=>
    string(4) "1387"
  }
}*/

  function get_formatted_object_for_transactions($transaction_list){
    $results = array('transactions' => array(),'times' => array());
    foreach($transaction_list as $transaction_id){
      $files_obj = $this->get_files_for_transaction($transaction_id);
      $groups_obj = $this->get_groups_for_transaction($transaction_id);
      // $files_obj = array('treelist' => array(), 'files' => array());
      // var_dump($files_obj);
      if(!empty($files_obj['treelist'])){
        $file_tree = $files_obj['treelist'];
        $flat_list = $files_obj['files'];
        foreach($flat_list as $item){
          $sub_time = new DateTime($item['stime']);
          break;
        }
        $time_string = $sub_time->format('Y-m-d H:i:s');
    
        $results['times'][$time_string] = $transaction_id;
        
        // $results['transactions'][$transaction_id]['files'] = $file_tree;
        // $results['transactions'][$transaction_id]['flat_files'] = $flat_list;
        if(sizeof($files_obj)>0){
          $status_list = $this->get_status_for_transaction('transaction',$transaction_id);
          // var_dump($status_list);
          if(sizeof($status_list) > 0){
            $results['transactions'][$transaction_id]['status'] = $status_list;
          }else{
            $results['transactions'][$transaction_id]['status'] = array();
          }
          if(sizeof($groups_obj) > 0){
            $results['transactions'][$transaction_id]['groups'] = $groups_obj['groups'][$transaction_id];
          }else{
            $results['transactions'][$transaction_id]['groups'] = array();
          }
        }
      }
    }
    if(!empty($results['times'])){
      arsort($results['times']);
    }
    // var_dump($results);
    return $results;
  }
  
  
  
  function get_job_status($job_id_list, $status_list = false){
    $status_list = !empty($status_list) ? $status_list : $this->status_list;
    $DB_myemsl = $this->load->database('default',TRUE);
    $select_array = array(
      'jobid', 'min(trans_id) as trans_id', 'max(step) as step', 'max(person_id) as person_id'
    );
    $DB_myemsl->select($select_array)->where_in('jobid',$job_id_list)->group_by('jobid');
    $query = $DB_myemsl->get('ingest_state');
    $results = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        $item = array(
          'state_name' => $status_list[$row->step],
          'state' => $row->step,
          'person_id' => $row->person_id
        );
        $results[$row->jobid] = $item;
      }
    }
    return $results;
  }
  
//select jobid, min(trans_id) as trans_id, max(step) as step from myemsl.ingest_state group by jobid order by jobid desc limit 50;
  

  function get_status_for_transaction($lookup_type, $id_list){
    $lookup_types = array(
      't' => 'trans_id', 'trans_id' => 'trans_id',
      'j' => 'jobid', 'job' => 'jobid'
    );
    if(!array_key_exists($lookup_type,$lookup_types)){
      $lookup_field = 'trans_id';
    }else{
      $lookup_field = $lookup_types[$lookup_type];
    }
    $DB_myemsl = $this->load->database('default',TRUE);
    $status_list = array();
    $select_array = array(
      'jobid','trans_id','person_id','step','message','status'
    );
    $DB_myemsl->trans_start();
    $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");    
    $DB_myemsl->select($select_array)->where_in($lookup_field,$id_list);
    $ingest_query = $DB_myemsl->get('ingest_state');
    $DB_myemsl->trans_complete();
    if($ingest_query && $ingest_query->num_rows()>0){
      foreach($ingest_query->result_array() as $row){
        if(intval($row['step']) >= 5 && strtoupper($row['status']) == 'SUCCESS' && $row['trans_id'] != -1){
          //need to check for validation progress
          $DB_myemsl->select('transaction')->group_by('transaction');
          $DB_myemsl->having("every(verified = 't')")->where('transaction', $row['trans_id']);
          $validation_query = $DB_myemsl->get('files');
          if($validation_query && $validation_query->num_rows() > 0){
            //looks like every file has been validated
            $row['step'] = 6;
            $row['status'] = 'SUCCESS';
            $row['message'] = 'verified';
          }
        }
        $status_list[$row[$lookup_field]][$row['step']] = $row;
        
      }
    }
   
    return $status_list;
  }
  
  function get_instrument_for_id($lookup_type,$id){
    $lookup_types = array(
      't' => 'trans_id', 'trans_id' => 'trans_id',
      'j' => 'jobid', 'job' => 'jobid'
    );
    if(!array_key_exists($lookup_type,$lookup_types)){
      $lookup_field = 'trans_id';
    }else{
      $lookup_field = $lookup_types[$lookup_type];
    }
    if($lookup_field == 'jobid'){
      $tx_info = $this->get_transaction_info($id);
      $id = $tx_info['transaction_id'];
      $lookup_field = 'trans_id';
    }
    
    $DB_myemsl = $this->load->database('default',TRUE);
    $inst_id = false;
    $query = $DB_myemsl->select('group_id as instrument_id')->get_where('v_transactions_by_group_id', array('transaction_id' => $id),1);
    if($query && $query->num_rows() > 0){
      $inst_id = $query->row()->instrument_id;
    }
    return $inst_id;
  }
  
  
  
  
  
  function get_transaction_info($job_id){
    $DB_myemsl = $this->load->database('default',TRUE);
    $DB_myemsl->trans_start();
    $DB_myemsl->query("set local timezone to '{$this->local_timezone}';");    
    $query = $DB_myemsl->select('trans_id as transaction_id')->get_where('ingest_state',array('jobid' =>$job_id),1);
    $DB_myemsl->trans_complete();
    $transaction_id = -1;
    if($query && $query->num_rows()>0){
      $transaction_id = !empty($query->row()->transaction_id) ? $query->row()->transaction_id : -1;
      $current_step = !empty($query->row()->step) ? $query->row()->step : 0;
    }
    return array('transaction_id' => $transaction_id, 'current_step' => $current_step);
  }
  

}
?>