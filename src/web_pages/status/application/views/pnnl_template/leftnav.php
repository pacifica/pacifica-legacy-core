<?php 
$first_used = false;
$current_page = $current_page_info['uri'];
?>
<div id="leftNav">
  <?php foreach ($categories as $index=>$category): ?>
  <?php 
  if(!$first_used){
    $class = " class=\"first\"";
    //$class="";
    $first_used = true;
  }else{
    $class = "";
  }
  ?>
  <h2<?= $class?>><?= $category['name']?></h2>
  <ul>
    <?php foreach ($category['entries'] as $entry_index=>$entry): ?>
    <?php 
    if($current_page == $entry['uri']){
      $entryclass = " class=\"selected\"";
      //$pagetext = "<strong>".$entry['name']."</strong>";
      $pagetext = $entry['name'];
    }else{
      $entryclass = " class=\"unselected\"";
      $pagetext = $entry['name'];
    }
    ?>
    <li<?= $entryclass?>>
      <a href="<?=base_url().$entry['uri']?>" id="<?=$entry_index?>"><?= $pagetext?></a>
    </li>
    <?php endforeach; ?>
  </ul>
  <?php $first_used = true; ?>
  <?php endforeach; ?>
</div>
