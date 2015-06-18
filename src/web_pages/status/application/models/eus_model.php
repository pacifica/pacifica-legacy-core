<?php
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     EUS_Model                                                               */
/*                                                                             */
/*             functionality for dealing with EUS supplied data                */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class Eus_model extends CI_Model {
  
  function __construct(){
    parent::__construct();
    define("INST_TABLE",'UP_INSTRUMENTS');
    define("INST_PROPOSAL_XREF", "UP_PROPOSAL_INSTRUMENTS");
    define("PROPOSALS_TABLE", "UP_PROPOSALS");
    define("PROPOSAL_MEMBERS", "UP_PROPOSAL_MEMBERS");
    define("USERS_TABLE", "UP_USERS");
  }
  
  function get_ers_instruments_list($unused_only = false, $filter = ""){
    $DB_ers = $this->load->database('eus_for_myemsl',TRUE);
    
    $select_array = array(
      'instrument_id',
      'instrument_name as instrument_description',
      'name_short as instrument_name_short',
      'COALESCE(`eus_display_name`,`instrument_name`) as display_name',
      'last_change_date as last_updated'
    );
    
    if(!empty($filter)){
      //check for numeric only and use in instrument_id?
      $DB_ers->like('instrument_name',$filter);
      $DB_ers->or_like('name_short',$filter);
      $DB_ers->or_like('eus_display_name',$filter);
    }

    $DB_ers->select($select_array,TRUE)->where('active_sw','Y');
    $DB_ers->order_by('eus_display_name');
    if($unused_only){
      
    }
    
    $query = $DB_ers->get(INST_TABLE);
    $results = array();
    $categorized_results = array();
    
    if($query && $query->num_rows()>0){
      foreach($query->result_array() as $row){
        $inst_id = $row['instrument_id'];
        unset($row['instrument_id']);
        $results[$inst_id] = $row;
        $display_name_info = explode(":",$row['display_name']);
        $display_name_type = sizeof($display_name_info)>1 ? array_shift($display_name_info) : "";
        $row['display_name'] = trim($display_name_info[0]); 
        $inst_info = explode(":",$row['instrument_description']);
        $inst_type = sizeof($inst_info) > 1 ? array_shift($inst_info) : "Other";
        $inst_desc = trim($inst_info[0]);
        
        $row['instrument_description'] = $inst_desc;
        $categorized_results[$inst_type][$inst_id] = $row;
        
        
      }
    }
    return $categorized_results;
  }

  function get_eus_user_list($filter = ""){
    $DB_ers = $this->load->database('eus_for_myemsl',TRUE);
    
    $select_array = array(
      'person_id as eus_id', 'first_name', 'last_name', 'email_address'
    );
    
    if(!empty($filter)){
      $DB_ers->like('first_name', $filter)->or_like('last_name', $filter)->or_like('email_address',$filter);
    }
    
    $query = $DB_ers->select($select_array)->get(USERS_TABLE);
    
    $results_array = array(
      'success' => FALSE,
      'message' => "No EUS users found using the filter '*{$filter}*'",
      'names' => array()
    );
    
    if($query && $query->num_rows() > 0){
      $plural_mod = $query->num_rows() > 1 ? "s" : "";
      $results_array['message'] = $query->num_rows()." EUS user{$plural_mod} found with filter '*{$filter}*'";
      $results_array['success'] = TRUE;
      foreach($query->result() as $row){
        $display_name = ucwords("{$row->first_name} {$row->last_name}");
        $display_name .= !empty($row->email_address) ? " <{$row->email_address}>" : "";
        $name_components = array(
          'first_name' => $row->first_name,
          'last_name' => $row->last_name,
          'email_address' => $row->email_address
        );
        foreach(array_keys($name_components) as $key_name){
          $comp = $name_components[$key_name];
          $comp = preg_replace("/(.*)({$filter})(.*)/i", '$1<span class="hilite">$2</span>$3',$comp);
          $marked_components[$key_name] = $comp;
        }
        $marked_up_display_name = ucwords("{$marked_components['first_name']} {$marked_components['last_name']}");
        $marked_up_display_name .= !empty($name_components['email_address']) ? " <{$marked_components['email_address']}>" : "";
     
        $results_array['names'][$row->eus_id] = array(
          'eus_id' => $row->eus_id,
          'first_name' => ucfirst($row->first_name),
          'last_name' => ucfirst($row->last_name),
          'email_address' => $row->email_address,
          'display_name' => $display_name,
          'marked_up_display_name' => $marked_up_display_name
        );
      }
    }
    return $results_array;
  }

  function get_instruments_for_proposal($eus_proposal_id, $filter = ""){
    $DB_ers = $this->load->database('eus_for_myemsl', TRUE);

    $result_array = array(
      'success' => FALSE,
      'message' => "",
      'instruments' => array()
    );

    $closing_date = new DateTime();
    $closing_date->modify("-6 months");
    
    // print_r($closing_date);
    
    $where_array = array(
      'proposal_id' => $eus_proposal_id,
      'actual_end_date <' => $closing_date->format('Y-m-d')
    );
    $DB_ers->where($where_array);
    
    $prop_exists = $DB_ers->count_all_results(PROPOSALS_TABLE) > 0 ? TRUE : FALSE;
    
    if(!$prop_exists){
      $result_array['message'] = "No proposal with ID = {$eus_proposal_id} was found";
      return $result_array;
    }
    
    $instrument_list = array();
    
    $select_array = array(
      'i.instrument_id', 'i.eus_display_name'
    );
    
    $DB_ers->select($select_array)->from(INST_TABLE." i");
    $DB_ers->join(INST_PROPOSAL_XREF." pi", "i.instrument_id = pi.instrument_id");
    
    if(!empty($filter)){
      $DB_ers->like('i.eus_display_name',$filter);
    }

    $inst_query = $DB_ers->get();
    
    if($inst_query && $inst_query->num_rows() > 0){
      $plural_mod = $inst_query->num_rows() > 1 ? "s" : "";
      $result_array['success'] = TRUE;
      $result_array['message'] = $inst_query->num_rows()." instrument{$plural_mod} located for proposal {$eus_proposal_id}";
      foreach($inst_query->result() as $row){
        $result_array['instruments'][$row->instrument_id] = $row->eus_display_name;
      }
    }else{
      $result_array['message'] = "No instruments located for proposal {$eus_proposal_id}";
    }
    
    return $result_array;
    
  }


  function get_proposals_for_instrument($eus_instrument_id, $filter = ""){
    $DB_ers = $this->load->database('eus_for_myemsl',TRUE);
    
    //check that instrument_id is legal and active
    $where_array = array(
      'active_sw' => 'Y',
      'instrument_id' => $eus_instrument_id
    );
    $inst_exists = $DB_ers->where($where_array)->count_all_results(INST_TABLE) > 0 ? TRUE : FALSE;
    
    $result_array = array('success' => FALSE);
    
    if(!$inst_exists){
      $result_array['message'] = "No instrument with ID = ".$eus_instrument_id." was found";
      $result_array['proposals'] = array();
      return $result_array;
      
    }
    $today = new DateTime();
    
    $select_array = array('pi.proposal_id', 'p.title as proposal_name');
    $DB_ers->select($select_array)->where('pi.instrument_id', $eus_instrument_id)->order_by('p.title');
    $DB_ers->where('p.closed_date is null')->where('p.actual_end_date >=', $today->format('Y-m-d'));
    $DB_ers->from(INST_PROPOSAL_XREF." as pi");
    $DB_ers->join(PROPOSALS_TABLE." as p", "p.proposal_id = pi.proposal_id");
    if(!empty($filter)){
      $DB_ers->like('p.title',$filter);
    }
    $proposal_query = $DB_ers->get();
            
    $proposal_list = array();
    if($proposal_query && $proposal_query->num_rows() > 0){
      $plural_mod = $proposal_query->num_rows > 1 ? "s" : "";
      $result_array['success'] = TRUE;
      $result_array['message'] = $proposal_query->num_rows()." proposal{$plural_mod} located for instrument {$eus_instrument_id}";
      foreach($proposal_query->result() as $row){
        $clean_proposal_name = trim(str_replace("\n", " ", $row->proposal_name));
        $proposal_list[$row->proposal_id] = $clean_proposal_name;
      }
    }else{
      $result_array['message'] = "No proposals located for instrument ".$eus_instrument_id;
    }
    $result_array['items'] = $proposal_list;
    return $result_array;
  }

  function get_proposal_name($eus_proposal_id){
    $DB_ers = $this->load->database('eus_for_myemsl', TRUE);
    $query = $DB_ers->select('title as proposal_name')->get_where(PROPOSALS_TABLE,array('proposal_id' => $eus_proposal_id),1);
    // echo $DB_ers->last_query();
    if($query && $query->num_rows() > 0){
      $result = $query->row()->proposal_name;
    }
    return $result;
  }


  function get_name_from_eus_id($eus_id){
    $DB_ers = $this->load->database('eus_for_myemsl',TRUE);
    $select_array = array(
      'person_id as eus_id', 'first_name', 'last_name', 'email_address'
    );
    $result = array();
    $query = $DB_ers->select($select_array)->get_where(USERS_TABLE, array('person_id' => $eus_id),1);
    if($query && $query->num_rows()>0){
      $result = $query->row_array();
    }
    return $result;
  }
  
  function get_proposals_for_user($eus_user_id){
    $DB_ers = $this->load->database('eus_for_myemsl',TRUE);
    $select_array = array('proposal_id','person_id');
    $DB_ers->select($select_array)->where('active','Y');
    
    $query = $DB_ers->get(PROPOSAL_MEMBERS);
    
    $results = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        $results[] = $row->person_id;
      }
    }
    return $results;
  }
  
  function get_user_instrument_proposal_overlap($eus_user_id, $eus_instrument_id, $eus_proposal_id){
    //get proposals for user
    $proposals_for_user = $this->get_proposals_for_user($eus_user_id);
    
    //get instruments for proposals
    $instruments_for_proposals = array();
    foreach($proposals_for_user as $eus_proposal_id){
      $instruments_for_proposals[$eus_proposal_id] = $this->get_instruments_for_proposal($eus_proposal_id);
    }
    
    
    
    
  }
  
  
}