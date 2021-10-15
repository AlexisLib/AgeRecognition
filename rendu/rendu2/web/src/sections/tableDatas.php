<div class="row">
    <div class="col s10 offset-s1">
        <ul class="tabs" id="tableDatas">
            <li class="tab col s4"><a href="#age">Age</a></li>
            <li class="tab col s4"><a href="#genre">Genre</a></li>
            <li class="tab col s4"><a href="#race">Origine</a></li>
        </ul>
    </div>
</div>

<div class="row" id="age">
    <div class="col s10 offset-s1">
        <table class="centered">
            <thread>
                <tr>
                    <th class="center">0-19</th>
                    <th class="center">20-39</th>
                    <th class="center">40-59</th>
                    <th class="center">60-79</th>
                    <th class="center">80-116</th>
                </tr>
            </thread>
            <tbody>
                <tr>
                    <td> <?php echo $dataset->{'0-19'} . " / " . round($dataset->{'0-19'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'20-39'} . " / " . round($dataset->{'20-39'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'40-59'} . " / " . round($dataset->{'40-59'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'60-79'} . " / " . round($dataset->{'60-79'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'80-116'} . " / " . round($dataset->{'80-116'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<div class="row" id="genre">
    <div class="col s10 offset-s1">
        <table class="centered">
            <thread>
                <tr>
                    <th class="center">Homme</th>
                    <th class="center">Femme</th>
                </tr>
            </thread>
            <tbody>
                <tr>
                    <td> <?php echo $dataset->{'numberMen'} . " / " . round($dataset->{'numberMen'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'numberWomen'} . " / " . round($dataset->{'numberWomen'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<div class="row" id="race">
    <div class="col s10 offset-s1">
        <table class="centered">
            <thread>
                    <th class="center">Caucasienne</th>
                    <th class="center">Afriacaine</th>
                    <th class="center">Asiatique</th>
                    <th class="center">Indienne</th>
                    <th class="center">Autres</th>
                </tr>
            </thread>
            <tbody>
                <tr>
                    <td> <?php echo $dataset->{'white'} . " / " . round($dataset->{'white'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'black'} . " / " . round($dataset->{'black'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'asian'} . " / " . round($dataset->{'asian'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'indian'} . " / " . round($dataset->{'indian'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                    <td> <?php echo $dataset->{'other'} . " / " . round($dataset->{'other'} / $dataset->{"numberPictures"} *100).'%'; ?></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
   

<script type="text/javascript">
    var el = document.getElementById("tableDatas")
    var instance = M.Tabs.init(el, []);
</script>
