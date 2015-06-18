<?php
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                             */
/*     Navigation Info Model                                                   */
/*                                                                             */
/*             functionality for setting up left hand nav menu                 */
/*                                                                             */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
$nav_info = null;
class Navigation_info_model extends CI_Model {
  function __construct(){
    parent::__construct();
    $this->load->helper(array('inflector'));    
    define('NAV_INFO_TABLE','v_navigation_info');
  }
  
  function generate_navigation_entries($current_path_info = "./"){
    $DB_wsi = $this->load->database('ws_info', TRUE);
    $equipment_listed = false;
    $DB_wsi->not_like('entry','List of Available');
    $DB_wsi->where("(`site_id` = {$this->site_id} or `site_id` = 0)");
    $where_array = array(
      'enabled' => true,
      'req_access_level <=' => $this->admin_access_level
    );
    if(ENVIRONMENT == 'production'){
      $where_array['dev_only'] = 0;
    }
    $query = $DB_wsi->get_where(NAV_INFO_TABLE,$where_array);
    $current_cat = false;
    $equipment_list = $this->get_equipment_types($this->site_id);
    $nav_info = array();
    foreach($query->result() as $row){
      $current_uri = $row->uri;
      $current_uri = rtrim($current_uri,'/');
      if($current_uri == rtrim($current_path_info,'/')) {
        $current_page_info = array('name' => $row->entry, 'uri' => $current_uri);
      }
      if($current_cat != $row->category){
        $current_cat = $row->category;
        $current_sorting_index = 'category_'.$row->category_display_order;
        $nav_info[$current_sorting_index] = array('name' => $current_cat,'entries' => array());
        if($row->category_description != null) {
          $nav_info[$current_sorting_index]['description'] = $row->description;
        }
      }

         
      $nav_info[$current_sorting_index]['entries']['entry_'.$row->category_display_order.".".$row->entry_display_order] = 
        array(
          'name' => $row->entry,
          'uri' => $current_uri,
          'alt_text' => $row->alt_text);
      if($current_cat == "Equipment / Software"){
        $new_display_order = $row->entry_display_order;
        foreach($equipment_list as $equip_type => $equip_info){
          $desc_array = explode(" ",$equip_info['description']);
          $last_word = plural(array_pop($desc_array));
          array_push($desc_array,$last_word);
          $equip_desc = implode(" ",$desc_array)." [{$equip_info['counts']}]";
          
          $new_display_order++;
          $nav_info[$current_sorting_index]['entries']["entry_{$row->category_display_order}.{$new_display_order}"] = 
            array(
              'name' => "List of {$equip_desc}",
              'uri' => "equipment/{$equip_type}",
              'alt_text' => ""
            );
        }
      }
    }
    if(!isset($current_page_info)){
      $current_page_info = array('name' => 'Undefined Page', 'uri' => $current_path_info);
    }
    return array('categories' => $nav_info,
      'current_page_info' => $current_page_info);
  }

  public function get_equipment_types($site_id){
    $DB_data = $this->load->database('default',TRUE);
    $DB_data->select(array("type","description","item_count"))->where('site_id',$site_id)->order_by("description");
    $query = $DB_data->get("v_equipment_list_w_counts");
    $equipment_list = array();
    if($query && $query->num_rows() > 0){
      foreach($query->result() as $row){
        $equipment_list[$row->type] = array('description' => $row->description, 'counts' => $row->item_count);
      }
    }
    return $equipment_list;
  }
  
  public function get_site_identifier($site_id){
    $DB_data = $this->load->database('default',TRUE);
    $DB_data->select(array('name','description','ticket_identifier'));
    $DB_data->where("`deleted_at` is null")->where('site_id',$site_id);
    $query = $DB_data->get('ticket_tracker_sites',1);
    $res = array();
    if($query && $query->num_rows() > 0){
      $res = array('name' => $query->row()->name, 'description' => $query->row()->description);
    }
    return $res;
  }

  
}
?>
