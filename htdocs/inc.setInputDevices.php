<ul class="list-group">
  <li class="list-group-item">
	<div class="row">
		<div class="col-xs-6">
<?php
$advancedrotarycontrolstatus = exec("/bin/systemctl status phoniebox-advanced-rotary-control.service | grep running");
if ($advancedrotarycontrolstatus != "") {
	print $lang['globalAdvancedRotaryControl'].' <span class="label label-success">'.$lang['globalEnabled'].'</span>';
	print '</div><!-- / .col-xs-6 -->';
	print '<div class="col-xs-6">';
	print "<a href='?advancedrotarycontrolstatus=turnoff' class='btn btn-sm btn-danger'><i class='mdi mdi-cancel'></i> ".$lang['globalSwitchOff']."</a>";
}
else {
	print $lang['globalAdvancedRotaryControl'].' <span class="label label-danger">'.$lang['globalDisabled'].'</span>';
	print '</div><!-- / .col-xs-4 -->';
	print '<div class="col-xs-4">';
	print "<a href='?advancedrotarycontrolstatus=turnon' class='btn btn-sm btn-success'><i class='mdi mdi-play'></i> ".$lang['globalSwitchOn']."</a>";
}
?>
		</div><!-- / .col-xs-6 -->
	</div><!-- / .row -->
  </li>

  <li class="list-group-item">
	<div class="row">
		<div class="col-xs-6">
<?php
$rfidstatus = exec("/bin/systemctl status phoniebox-rfid-reader.service | grep running");
if ($rfidstatus != "") {
	print $lang['globalRfidReader'].' <span class="label label-success">'.$lang['globalEnabled'].'</span>';
	print '</div><!-- / .col-xs-6 -->';
	print '<div class="col-xs-6">';
	print "<a href='?rfidstatus=turnoff' class='btn btn-sm btn-danger'><i class='mdi mdi-cancel'></i> ".$lang['globalSwitchOff']."</a>";
}
else {
	print $lang['globalRfidReader'].' <span class="label label-danger">'.$lang['globalDisabled'].'</span>';
	print '</div><!-- / .col-xs-4 -->';
	print '<div class="col-xs-4">';
	print "<a href='?rfidstatus=turnon' class='btn btn-sm btn-success'><i class='mdi mdi-play'></i> ".$lang['globalSwitchOn']."</a>";
}
?>
		</div><!-- / .col-xs-6 -->
	</div><!-- / .row -->
  </li>
</ul>
