
import cv2 #importé pour utiliser OpenCV pour le traitement d'image
import easygui #importé pour ouvrir une boîte de fichiers. 
#Cela nous permet de sélectionner n'importe quel fichier de notre système.
import numpy as np  #les images sont stockées et traitées sous forme de nombres. Ceux-ci sont considérés comme des tableaux.
# Nous utilisons NumPy pour traiter les tableaux.
import imageio #Utilisé pour lire l'image qui est choisi par boîte de fichier en utilisant un chemin.

import sys
import matplotlib.pyplot as plt #Cette bibliothèque est utilisée pour la visualisation et le traçage.
import os #pour l'interaction avec le système d'exploitation. 
#Ici, pour lire le chemin et enregistrer les images sur ce chemin
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image



top=tk.Tk()
top.geometry('700x700')
top.title('Cartoonify an Image by Hind Abouche')
top.configure(background='gray')
label=Label(top,background='gray', font=('Courier New',40,'bold'))



def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # lire l'image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    # l'image est stockée sous forme de nombres

    # confirmer que l'image est choisie
    if originalmage is None:
        print("Impossible de trouver une image. Choisissez le fichier approprié")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')


    #convertir l'image en niveau de grie
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


    #application d'un flou médian pour lisser une image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #récupération des bords pour un effet de dessin animé en utilisant la technique de seuillage
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')



    #application d'un filtre bilatéral pour éliminer le bruit et gardez les bords nets au besoin
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #masquage de l'image bordée avec notre image "BEAUTIFY"
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized6, cmap='gray')




    # Tracer toute la transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Cliquez ici si vous voulez enregistrer le dessin animé de l'image",command=lambda: save(ReSized6, ImagePath),padx=50,pady=5)
    save1.configure(background='pink', foreground='blue',font=('Courier New',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(ReSized6, ImagePath):
    #enregistrement d'une image en utilisant imwrite ()
    newName="Image_caricaturée"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image enregistrée par nom " + newName +" dans "+ path
    tk.messagebox.showinfo(title='Abouche Hind', message=I)


upload=Button(top,text="cliquez ici pour choisir ton image",command=upload,padx=10,pady=5)
upload.configure(background='pink', foreground='blue',font=('Courier New',10,'bold'))
upload.pack(side=TOP,pady=50)


top.mainloop()



