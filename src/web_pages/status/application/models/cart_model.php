<?php
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     Cart Model                                                              */
/*                                                                             */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class Cart_model extends CI_Model {
  function __construct(){
    parent::__construct();
    $this->local_timezone = "US/Pacific";
    $this->load->helper(array('user','item','time'));
    $this->user_id = get_user();
    
    define("CART_TABLE", 'cart');
    define("ITEMS_TABLE", 'cart_items');
    define("CART_URL_BASE", '/myemsl/cart/download/');
  }
  
  function get_active_carts($eus_id, $show_expired = true, $new_tx_id = false){
    $DB_myemsl = $this->load->database('default',true);
    $select_array = array(
      'cart_id', 'submit_time', 'last_mtime as modification_time',
      'last_email as last_email_time','state',
      'size as size_in_bytes', 'items as item_count'
    );
    $state_array = array(
      'admin_notified' => 'admin',
      'ingest' => 'unsubmitted',
      'submitted' => 'building',
      'amalgam' => 'building',
      'downloading' => 'building',
      'email' => 'available',
      'download_expiring' => 'expired',
      'expiring' => 'expired',
      'expired' => 'expired',
    );
    $cart_list = array();
    $accepted_states = array(
      'amalgam','downloading','email','admin_notified','submitted'
      // 'expiring','expired','download_expiring'
    );
    // if($show_expired){
      // $accepted_states[] = 'expiring';
      // $accepted_states[] = 'expired';
      // $accepted_states[] = 'download_expiring';
    // }
    $DB_myemsl->select($select_array)->where('person_id',$eus_id)->order_by('last_mtime desc');
    $query = $DB_myemsl->where_in('state',$accepted_states)->get(CART_TABLE);
    if($query && $query->num_rows()>0){
      foreach($query->result() as $row){
        $display_state = array_key_exists($row->state, $state_array) ? $state_array[$row->state] : "unknown";
        $display_size = format_bytes($row->size_in_bytes);
        $cart_id = $row->cart_id;
        $submit_time = new DateTime($row->submit_time);
        $modified_time = new DateTime($row->modification_time);
        
        $email_time = new DateTime($row->last_email_time);
        $cart_list[$display_state][$row->cart_id] = array(
          'cart_id' => $row->cart_id, 'raw_state' => $row->state,
          'display_state' => $display_state, 'size_bytes' => $row->size_in_bytes,
          'display_size' => $display_size, 
          'item_count' => 0,
          'times' => array(
            'submit' => $row->submit_time,
            'modified' => $row->modification_time,
            'email' => $row->last_email_time,
            'submit_time_obj' => $submit_time,
            'modified_time_obj' => $modified_time,
            'email_time_obj' => $email_time,
            'formatted_submit' => format_cart_display_time_element($submit_time),
            'formatted_modified' => format_cart_display_time_element($modified_time),
            'formatted_email' => format_cart_display_time_element($email_time),
            'generation_time' => friendlyElapsedTime($submit_time,$email_time,false)
          )
        );
        $cart_items_query = $DB_myemsl->select('item_id')->get_where(ITEMS_TABLE,array('cart_id' => $cart_id));
        $cart_item_list = array();
        $metadata = array(
          'proposal_id' => "None Specified", 'proposal_description' => "No Proposal Specified",
          'instrument_id' => "None Specified", 'instrument_description' => "No Instrument Specified"
        );
        if($cart_items_query && $cart_items_query->num_rows() > 0){
          foreach($cart_items_query->result() as $ci_row){
            $cart_item_list[] = $ci_row->item_id;
          }
        }
        if(!empty($cart_item_list)){
          $item_count = sizeof($cart_item_list);
          $cart_list[$display_state][$row->cart_id]['item_count'] = $item_count;
          $item_count_pluralizer = $item_count != 1 ? "s" : "";
          $cart_list[$display_state][$row->cart_id]['display_item_count'] = "{$item_count} item{$item_count_pluralizer}";
          $inst_matcher = "/Instrument\.(\d+)/i";
          $md_select_array = array('g.name','g.type');
          $DB_myemsl->select($md_select_array)->distinct();
          $DB_myemsl->from('groups g')->join('group_items gi','g.group_id = gi.group_id');
          $metadata_query = $DB_myemsl->where_in('gi.item_id',$cart_item_list)->get();
          if($metadata_query && $metadata_query->num_rows() > 0){
            foreach($metadata_query->result() as $md_row){
              $type = $md_row->type;
              $name = $md_row->name;
              if(preg_match($inst_matcher,$type,$inst_matches)){
                $metadata['instrument_id'] = $inst_matches[1];
                $metadata['instrument_description'] = $name;
              }elseif(strtolower($type) == 'proposal'){
                $metadata['proposal_id'] = $name;
              }
            }
          }
          $DB_myemsl->select(array('max(t.transaction) as tx_id', 'max(t.stime) as upload_time'));
          $DB_myemsl->from('transactions t')->join('files f','f.transaction = t.transaction');
          $DB_myemsl->group_by('t.transaction')->where_in('f.item_id',$cart_item_list);
          $tx_query = $DB_myemsl->limit(1)->get();
          if($tx_query && $tx_query->num_rows()>0){
            $cart_list[$display_state][$row->cart_id]['transaction_id'] = $tx_query->row()->tx_id;
            $cart_list[$display_state][$row->cart_id]['times']['upload_time'] = $tx_query->row()->upload_time;
            $up_time = new DateTime($tx_query->row()->upload_time);
            $cart_list[$display_state][$row->cart_id]['times']['formatted_upload_time'] = $up_time->format('d M Y g:ia');
          }
        }
        $cart_list[$display_state][$row->cart_id]['metadata'] = $metadata;
        if($display_state == 'available'){
          $cart_url = CART_URL_BASE."{$this->user_id}/{$row->cart_id}.amalgam/{$row->cart_id}.tar";
          // echo "cart_id => {$row->cart_id} {$cart_url}\n";
          $cart_list[$display_state][$row->cart_id]['download_url'] = $cart_url;
        }
      }
    }
    return $cart_list;
  }
  
  
  
  
  function delete_dead_cart($cart_id){
    $DB_myemsl = $this->load->database('default',true);
    $success_info = array('success' => FALSE, 'message' => '');
    //make sure that this cart even exists.....
    $get_query = $DB_myemsl->get_where(CART_TABLE,array('cart_id' => $cart_id, 'state !=' => 'expired'),1);
    if($get_query && $get_query->num_rows() > 0){
      $cart_info = $get_query->row();
      $cart_create_time = new DateTime($cart_info->submit_time);
            
      //...and that we own the rights to it
      if($cart_info->person_id == $this->user_id){
        //looks like it's ours...
        if($cart_info->state != 'email'){
          //...and it's in a limbo-like state (admin_notified or ingest)
          $now_time = new DateTime();
          $new_data = array('state' => 'expired', 'last_mtime' => $now_time->format('Y-m-d H:i:s'));
          $delete_query = $DB_myemsl->where('cart_id',$cart_id)->where('person_id', $this->user_id)->update(CART_TABLE,$new_data);
          if($DB_myemsl->affected_rows() > 0){
            $success_info['success'] = TRUE;
            $success_info['message'] = "Cart #{$cart_id} (Submitted by User {$cart_info->person_id} on {$cart_create_time->format('d M Y g:ia')}) was successfully expired";
          }else{
            $success_info['message'] = "Cart #{$cart_id} could not be deleted because an error occurred";
          }
        }else{
          //...but it's in an inappropriate state that can't be deleted from here
          //  pass it along to the myemsl api???
          $success_info['message'] = "Cart #{$cart_id} could not be deleted using this mechanism. Use the Myemsl API.";
        }
      }else{
        //...but it's not ours
        //  throw an appropriate error
        $success_info['message'] = "Cart #{$cart_id} cannot be deleted, because it is not yours to delete";
      }
    }else{
      //cart either doesn't exist, or is already expired
      $success_info['message'] = "Cart #{$cart_id} cannot be deleted, because it is either doesn't exist, or is already expired";
    }
    return $success_info;
  }
  
  
}



?>