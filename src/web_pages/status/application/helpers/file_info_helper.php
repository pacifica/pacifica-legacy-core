<?php  if (!defined('BASEPATH')) exit('No direct script access allowed');
  
// function format_bytes($bytes) {
   // if ($bytes < 1024) return $bytes.' B';
   // elseif ($bytes < 1048576) return round($bytes / 1024, 2).' KB';
   // elseif ($bytes < 1073741824) return round($bytes / 1048576, 2).' MB';
   // elseif ($bytes < 1099511627776) return round($bytes / 1073741824, 2).' GB';
   // else return round($bytes / 1099511627776, 2).' TB';
// }

function quarter_to_range($quarter_num){
  $last_q = $quarter_num - 1;
  $this_q = $quarter_num;
  
  $first_month_num = $last_q * 3 + 1;
  $last_month_num = $this_q * 3;
  
  $first_month = get_month_string($first_month_num);
  $last_month = get_month_string($last_month_num);
  
  return "{$first_month}&ndash;{$last_month}";
 
}

function get_month_string($month_num){
  return date("M", mktime(0,0,0, $month_num, 1, 2012));
}


function generate_bread_crumbs($path, $controller, $method){
  $bc_parts = !empty($path) ? explode(DIRECTORY_SEPARATOR, $path) : array();
  $bc = array("Home" => "");
  if(sizeof($bc_parts) > 0) {
    foreach($bc_parts as $directory){
      $bc[$directory] = $directory;
    }
  }

  $root_path = $controller.DIRECTORY_SEPARATOR.$method;
  $bc_string = "";
  $bc_components = array();
  $path = rtrim($root_path,DIRECTORY_SEPARATOR);
  $counter = 0;
  foreach($bc as $name => $directory){
    $counter++;
    $path .= $directory.DIRECTORY_SEPARATOR;
    $link_bits = $counter == sizeof($bc) ? $name : anchor($path, $name, array("class" => "bc_link"));
    $bc_components[] = "<span class='bc_dirname'>{$link_bits}</span>";
  }
  $bc_string = implode("<span class='bc_divider'> &gt; </span>&nbsp", $bc_components);
  return $bc_string;
}

function is_file_on_tape($path){
  $on_tape = check_disk_stage($path,TRUE);
  $on_tape = $on_tape == 0 ? true : false;
  return $on_tape;
}


function check_disk_stage($path, $numeric = false){
  //fake it out until I get real support
  if($numeric){
    return 0;
  }else{
    return "on_tape";
  }
  $attr = exec("which attr");
  $status_attribute_name = "disk_stage_status";
  $attr_cmd = "{$attr} -g \"{$status_attribute_name}\" \"{$path}\"";
  $status_bit = exec($attr_cmd);
  $status_bit = intval($status_bit);

  $status = $status_bit == 0 ? "on_tape" : "on_disk";
  
  $status_bit = $numeric ? $status_bit : $status;
  
  return $status_bit;
}

function array_prefix_values($prefix, $array){
  $callback = create_function('$s','return "'.$prefix.'".$s;');
  return array_map($callback,$array);
}

function get_last_update(){
  if ( func_num_args() < 1 ) return 0;
  $dirs = func_get_args();
  $files = array();
  foreach ( $dirs as $dir )
  {
    // $directory = new RecursiveDirectoryIterator($dir);
    $objects = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir),RecursiveIteratorIterator::LEAVES_ONLY);
    $files = array_keys(iterator_to_array($objects,TRUE));
  }
  $maxtimestamp = 0;
  $maxfilename = "";
  foreach ( $files as $file )
  {
    $timestamp = filemtime($file);
    if ( $timestamp > $maxtimestamp )
    {
      $maxtimestamp = $timestamp;
      $maxfilename = $file; 
    }
  }
  $d = new DateTime();
  $d->setTimestamp($maxtimestamp);
  return $d;
}

