<div class="row">
    <div class="col s8 offset-s2">
        <div class="card horizontal">
            <div class="card-image">
                <img id="picture" src="img/placeholder.jpg">
            </div>
            <div class="card-stacked">
                <div class="card-content">
                    <p><br>Sélectionnez la photo d'une personne dont vous souhaitez connaitre son âge : <br><br></p>
                    <form id="pictureForm" method="post" enctype="multipart/form-data">
                        <p>
                            <label for="fileToUpload" title="Recherchez le fichier à uploader !">Envoyer le fichier :</label>
                            <input type="hidden" name="MAX_FILE_SIZE" />
                            <input name="file" type="file" id="fileToUpload" />
                            <input style="display: none;" id="sendForm" type="submit" name="submit" value="Uploader" />
                        </p>
                    </form>
                </div>
                <div class="card-action">
                    <a href="javascript:simulateSendForm()" class="right blue-text">Déterminer l'âge</a>
                </div>
            </div>
        </div>
    </div>
</div>

<script type="text/javascript">

    function getResultsOld(){

        var xhr;

        try {  xhr = new ActiveXObject('Msxml2.XMLHTTP');   }
        catch (e) 
        {
            try {   xhr = new ActiveXObject('Microsoft.XMLHTTP'); }
            catch (e2) 
            {
               try {  xhr = new XMLHttpRequest();  }
               catch (e3) {  xhr = false;   }
             }
        }
      
        xhr.onreadystatechange  = function(){ 
           if(xhr.readyState  == 4){
                console.log(xhr.responseText); 
            }else{
               console.log(xhr.status);
            }
        }; 
 
   xhr.open("GET", "http://192.168.1.20:1111/results/",  true); 
   xhr.send(); 
} 

    function simulateSendForm(){
         document.getElementById("sendForm").click();
    }

    window.addEventListener("load", function () {
        function sendData() {

            var XHR = new XMLHttpRequest();

            // Liez l'objet FormData et l'élément form
            var FD = new FormData(form);

            // Définissez ce qui se passe si la soumission s'est opérée avec succès
            XHR.addEventListener("load", function(event) {
                //console.log(event.target.responseText);
                if(event.target.responseText[0] == "t" ){
                     M.toast({html: 'Upload réussi'});
                     document.getElementById("picture").src = event.target.responseText;
                     getResults()

                }else{
                    M.toast({html: event.target.responseText});
                }
            });

            // Definissez ce qui se passe en cas d'erreur
            XHR.addEventListener("error", function(event) {
              alert('Oups! Quelque chose s\'est mal passé.');
            });

            // Configurez la requête
            XHR.open("POST", "/src/sections/checkPicture.php" );

            // Les données envoyées sont ce que l'utilisateur a mis dans le formulaire
            XHR.send(FD);
        }

        // Accédez à l'élément form …
        var form = document.getElementById("pictureForm");

        // … et prenez en charge l'événement submit.
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            sendData();
        });
    });
</script>