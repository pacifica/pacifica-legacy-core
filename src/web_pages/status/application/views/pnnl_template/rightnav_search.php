<!--
<form id="siteSearch" method="get" action="http://search.pnl.gov/search">

  <div class="tab">
    <label for="siteSearchQ"><span>Search Site</span></label>
  </div>
  <div class="input">
    <input type="search" name="q" value="" id="siteSearchQ" title="Site-specific search" />
    <input type="image" id="siteSearchSubmit" src="https://css.pnl.gov/images/search_button.png" alt="Search" />
  <input type="hidden" name="as_sitesearch" value="brand.pnl.gov" /> 
  <input type="hidden" name="access" value="a" />
  <input type="hidden" name="output" value="xml_no_dtd" />
  <input type="hidden" name="client" value="default_frontend" />
  <input type="hidden" name="site" value="default_collection" />
  <input type="hidden" name="proxystylesheet" value="default_frontend" />
  <input type="hidden" name="as_dt" value="i" />
  </div>
</form>
 -->
<div id="rightCol">
  <h2>User Information</h2>
  <h3>Logged in as</h3>
  <p><?= anchor('/edit/my_user_details',$full_name, array('title'=>'Edit User Information')) ?></p>
  <h2>Additional Information</h2>
  <h3>Contacts</h3>
  <p>WebMaster<br /><a href="mailto:ken.auberry@pnl.gov" class="email">Ken Auberry</a></p>
</div>