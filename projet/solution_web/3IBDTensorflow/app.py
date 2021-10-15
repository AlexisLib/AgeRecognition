from flask import Flask, make_response, render_template, request, send_file, flash, send_from_directory, url_for
from mainML import getMLResults
from werkzeug import secure_filename
from utilsImage import *
from config import *
import json
from OpenSSL import SSL

app = Flask(__name__)
app.secret_key = 'd66HR8dgjYYic*dhfdsfsdf'
app.config['UPLOAD_FOLDER'] = DOSSIER_SAVE

@app.route('/', methods=['GET', 'POST'])
def accueil():
    results = None
    cardImage = "img/placeholder.png"

    if request.method == "POST":
        f = request.files['fic']
        if f:  # on vérifie qu'un fichier a bien été envoye
            if f.filename[-4:] == '.png' or f.filename[-5:] == ".jpeg" or f.filename[-4:] == ".gif" or f.filename[-4:] == ".jpg":
                namefile = secure_filename(f.filename)
                f.save(DOSSIER_SAVE + namefile)

                #preparation photo
                cardImage, resizeCropImg = get_path_image_clean(namefile)


                #lancer analyse ML
                if resizeCropImg is None:
                    results = getMLResults(pathImg=DOSSIER_SAVE+cardImage)
                else:
                    results = getMLResults(pathImg=DOSSIER_SAVE+cardImage, pathImgCrop=DOSSIER_SAVE+resizeCropImg)

                cardImage = "tmp/" + cardImage
        else:
            flash("Vous avez oublié le fichier !")

    return render_template('accueil.html', data=results, cardImage=cardImage )

@app.route("/avance/", methods=['GET', 'POST'])
def avance():
    results = None
    selectValues = None
    cardImage = "img/placeholder.png"

    with open("trainModels.json") as f:
        selectValues = json.load(f)

    if request.method == "POST":
        f = request.files['fic']
        modelChoose = request.form["selectModel"]

        if f.filename[-4:] == '.png' or f.filename[-5:] == ".jpeg" or f.filename[-4:] == ".gif" or f.filename[-4:] == ".jpg":
            namefile = secure_filename(f.filename)
            f.save(DOSSIER_SAVE + namefile)

            # preparation photo
            cardImage, resizeCropImg = get_path_image_clean(namefile)
            cardImage = "tmp/" + cardImage

            # lancer analyse ML
            results = getMLResults(pathImg=DOSSIER_SAVE+cardImage, pathImgCrop=DOSSIER_SAVE+resizeCropImg, modele=modelChoose)

        else:
            flash("Vous avez oublié le fichier !")
    return render_template('avance.html', data=results, selectValues=selectValues, cardImage=cardImage)

@app.errorhandler(404)
def page_non_trouvee(error):
    return  make_response("Cette page devrait vous avoir renvoyé une erreur 404", 404)


if __name__ == '__main__':

    #app.run(host='0.0.0.0', port=443, ssl_context=('certificats/boudeville.crt', 'certificats/boudeville.key') )
    app.run(port=80, debug=True)


