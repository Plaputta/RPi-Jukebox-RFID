<!--
Minimum Volume Select Form
-->
        <!-- input-group -->          
        <?php
        $maxvolumevalue = exec("/usr/bin/sudo ".$conf['scripts_abs']."/playout_controls.sh -c=getmaxvolume");
        $minvolumevalue = exec("/usr/bin/sudo ".$conf['scripts_abs']."/playout_controls.sh -c=getminvolume");
        $minvalueselect = round(($minvolumevalue/10))*10;
        $minvaluedisplay = round($minvolumevalue);
        ?>
        <div class="col-md-4 col-sm-6">
            <div class="row" style="margin-bottom:1em;">
              <div class="col-xs-6">
              <h4><?php print $lang['settingsMinVol']; ?></h4>
                <form name='minvolume' method='post' action='<?php print $_SERVER['PHP_SELF']; ?>'>
                  <div class="input-group my-group">
                    <select id="minvolume" name="minvolume" class="selectpicker form-control">
                    <?php
                    $i = 0;
                    while ($i <= $maxvolumevalue) {
                        print "
                        <option value='".$i."'";
                        if($minvalueselect == $i) {
                            print " selected";
                        }
                        print ">".$i."%</option>";
                        $i = $i + 10;
                    };
                    print "\n";
                    ?>
                    </select> 
                    <span class="input-group-btn">
                        <input type='submit' class="btn btn-default" name='submit' value='<?php print $lang['globalSet']; ?>'/>
                    </span>
                  </div>
                </form>
              </div>
              
              <div class="col-xs-6">
                  <div class="c100 p<?php print $minvaluedisplay; ?>">
                    <span><?php print $minvaluedisplay; ?>%</span>
                    <div class="slice">
                        <div class="bar"></div>
                        <div class="fill"></div>
                    </div>
                  </div> 
              </div>
            </div><!-- ./row -->
        </div>
        <!-- /input-group -->
