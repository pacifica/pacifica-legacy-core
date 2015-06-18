<?php 
if(!defined('BASEPATH'))
  exit('No direct script access allowed');
  
  function friendlyElapsedTime($datetime_object, $base_time_obj = false, $use_ago = true){
    date_default_timezone_set('America/Los_Angeles');
    
    if(!$base_time_obj) {
      $base_time_obj = new DateTime();
    }
    //convert to time object if string
    if(is_string($datetime_object)) { $datetime_object = new DateTime($time); }
    
    $nowTime = $base_time_obj;
    
    $diff = $nowTime->getTimestamp() - $datetime_object->getTimestamp();
    
    $result = "";
    
    //calc and subtract years
    $years = floor($diff/60/60/24/365);
    if($years > 0){ $diff -= $years*60*60*24*365; }
    
    //calc and subtract months
    $months = floor($diff/60/60/24/30);
    if($months > 0){ $diff -= $months*60*60*24*30; }
    
    //calc and subtract weeks
    $weeks = floor($diff/60/60/24/7);
    if($weeks > 0){ $diff -= $weeks*60*60*24*7; }
    
    //calc and subtract days
    $days = floor($diff/60/60/24);
    if($days > 0){ $diff -= $days*60*60*24; }
    
    //calc and subtract hours
    $hours = floor($diff/60/60);
    if($hours >0){ $diff -= $hours*60*60; }
    
    //calc and subtract minutes
    $min = floor($diff/60);
    if($min > 0){ $diff -= $min*60; }
    
    $qualifier = "about";
    
    
    
    if($years > 0){
//      $qualifier = $months > 1 ? "over" : "about";
      $unit = $years > 1 ? "years" : "year";
//      $years = $years == 1 ? "a" : $years;
      $result[] = "{$years} {$unit}";
    }
    if($months > 0){
//      $qualifier = $weeks > 1 ? "just over" : "about";
      $unit = $months > 1 ? "months" : "month";
//      $months = $months == 1 ? "a" : $months;
      $result[] = "{$months} {$unit}";
    }
    if($weeks > 0){
////      $qualifier = $days > 2 ? "about" : "about";
      $unit = $weeks > 1 ? "weeks" : "week";
      $result[] = "{$weeks} {$unit}";      
    }
    if($days > 0){
      $unit = $days > 1 ? "days" : "day";
//      $days = $days == 1 ? "a" : $days;
      $result[] = "{$days} {$unit}";      
    }
    if($hours > 0){
      $unit = $hours > 1 ? "hrs" : "hr";
//      $hours = $hours == 1 ? "a" : $hours;
      $result[] = "{$hours} {$unit}";      
    }
    if($min > 0){
//      $qualifier = $diff > 20 ? "a bit over" : "about";
      $unit = $min > 1 ? "min" : "min";
//      $min = $min == 1 ? "a" : $min;
      $result[] = "{$min} {$unit}";      
    }
    if($diff > 0){
      $unit = $diff > 1 ? "sec" : "sec";
      if(empty($result)){
        $result[] = "{$diff} {$unit}";
      }
    }else{
      $result[] = "0 seconds";
    }
    $ago = $use_ago ? " ago" : "";
    //format string
    $result_string = sizeof($result) > 1 ? "~".array_shift($result)." ".array_shift($result)."{$ago}" : "~".array_shift($result)."{$ago}"; 
    return $result_string;
  }

  function format_cart_display_time_element($time_obj){
    $elapsed_time = friendlyElapsedTime($time_obj);
    $formatted_time = $time_obj->format('d M Y g:ia');
    $iso_time = $time_obj->getTimestamp();
    
    return "<time title='{$formatted_time}' datetime='{$iso_time}'>{$elapsed_time}</time>";
    
  }
  
?>