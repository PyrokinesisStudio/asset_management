'''
29/11/2015 
Version 0_1: - creation de l'addon avec preview
             - import depuis la librairie
             - ajout a la librairie
             - creation auto des thumbnails et update manuel de la preview
             

01/12/2015 
Version 0_1_1: - ajout de l'update auto apres ajout d'un objet
               - popup pour choisir si le rendu du thumbnail se fait avec ou sans subsurf et smooth shading 


02/12/2015
Version 0_1_2: - ajout du remove, du replace_rename
               - modification de la scene de rendu et ajout d'une securite evitant aux gens de cliquer sur add ou remove le temps du rendu


04/12/2015
Version 0_1_5: - ajout du selecteur de categorie, de la possibiliter d'en creer de nouvelle et d'en supprimer


05/12/2015
Version 0_2: - merges des versions


06/12/2015
Version 0_2_4: - ajout des favoris et correction du bug d'ajout d'un objet a la librairie si on venait de supprimer ce meme objet de la librairie


07/12/2015
Version 0_2_5: - ajout du code de suppression du mesh lors du generate_thumbnail si jamais le mesh precedent n'a pas ete supprime
               - Ajout egalement du code pour placer le panel et T ou N ou les deux


08/12/2015
Version 0_2_6: - ajout de la customisation des thumbnails


10/12/2015
Version 0_2_7: - ajout du add to selection de la preview


13/12/2015
Version 0_2_8: - modification des preferences utilisateur
               - ajout du add_to_selection pour l'objet selectionne
               - ajustement du positionnement de l'objet ajoute pour qu'il corresponde bien aux normales de la face


15/12/2015
Version 0_2_9: - ajout du code pour pouvoir selectionner dans la preview sans faire l'import
               - ajout de la possibilite de pouvoir renommer les categories
               - ajout d'un raccourci pour appeler la preview depuis le viewport


16/12/2015
Version 0_3: - ajout du code pour pouvoir ajouter un groupe a la librairie et le supprimer


17/12/2015
Version 0_3_1: - modification du code pour eviter un join des objet qui aurait pu creer des problemes


18/12/2015
Version 0_3_1: - amelioration de l'ui et ajout de nouveaux icons


20/12/2015
Version 0_3_2: - reprise totale du code pour modifier le fonctionnemant de l'addon
               - mise en place des dossiers "library" et de dossiers "category" places dans les dossiers "library"
               - la partie du code pour l'ajout de groupe est pour l'instant supprimee
               - chaque asset possede son .blend
                

21/12/2015
Version 0_3_3: - suppression du popup a l'ajout d'un objet dans la librairie pour le placer dans le panel


28/12/2015
Version 0_3_4: - possibilite d'ajouter plusieur objets en meme temps avec rendu separes


01/01/2016
Version 0_3_5: - possibilite d'ajouter un groupe d'objet comme etant un seul asset
               - reintegration des keymaps pour la preview
               

02/01/2016
Version 0_3_6: - ajout des urls dans las prefs
               - ajout du code pour appliquer les modifiers pour les rendus
               - corrections de quelques bugs
               - ajout du menu popup dans la vue 3D (instable)
               

03/01/2016
Version 0_3_7: - correction de bugs notemment du au rendu (probleme d'application des transforms si objetc linkes, probleme d'application de modifieurs si desactive: subsurf)


05/01/2016
Version 0_3_8: - modification du code pour la creation du bbox (plus besoin d'appliquer les transforms)
               - ajout de l'integration de particules hair au bbox (fonctionne avec le render_type en PATH, encore des soucis evec le render_type OBJECT et GROUP)
               

06/01/2016
Version 0_3_9: - ajout de la transparance pour les rendu et donc, les thumbnails seront rendu en .png
               - modification de l'interface
               

07_01_2016
Version 0_4: - amelioration du "prepare asset" (reste a peaufiner)
             - ajout de la possibilite de choisir si on veut afficher les noms dans la preview ou pas
             - ajout de l'option du choix du mat pour les objets seul ayant deja un subsurf
             

13/01/2016
Version 0_4_1: - prise en compte des particules pour le bbox
               - correction du bug pour l'application du materiau si plusieurs slots
               - changement du fonctionnement des parametres "add_subsurf", "add_smooth" et "material" dans le panel d'ajout dans la lib qui concervent maintenat le choix precedent
               - ajout de l'ambient occlusion pour les thumbnails
               

14/01/2016
Version 0_4_2: - ajout du code pour les multi objets sur la selection
               - possibilite de choisir si on veut ajouter notre groupe d'asset en le parentant a un objet "main"
               - amelioration de l'AO pour les thumbnails
               

16/01/2016
Version 0_4_3: - correction des divers bugs a la creation de thumbnails
               - ajout du rendu freestyle
               - ajout d'un debug manuel en cas ou de thumbnail non rendu(sera a mettre en automatique)
               

16/01/2016
Version 0_4_4: - concervation des layer en fonction des objets


23/01/2016
Version 0_4_5: - corrections de bugs lors de l'ajout a la librairie
               - ajout de securites => si un .blend est vide, il ne sera pas sauvegarde et le rendu ne sera pas lance
               - modification du fonctionnement du add_to_selection en mode edit => concervation des modificateur et reste en mode objet une fois les assets ajoutes
               - correction du bug de rendu entre les particules group et les assets ayant des links
               - ajout d'un deuxieme prepare asset special HardOps
               
   
24/01/2016
Version 0_4_6: - amelioration du aply_shape_keys pour les rendus
               - prise en compte des objets de typr 'CURVE' ayant un bevel_depth ou un bevel_object ou un extrude
               - possibilite de choisir si on veut mettre un custom thumbnail en indiquant son emplacement avant ajout a la librairie
               
29/01/2016
Version 0_4_7: - placement des objets unique dans leur layers respectifs
               - camera non supprimee si on clic sur "cancel"
               - modification du code du "render" => passage en modal pour fermer le .blend de rendu une fois le thumbnail cree et le reouvrir pour rendre le suivant. Trouver une solution pour que les rendus se suivent sans que l'on ait besoin d'etre present pour creer un event.

           
02/02/2016
Version 0_4_8: - correction du bug du au chemin relatif pour les thumbnails avec choix d'image
               - amelioration du setup de l'opengl
               - debut de nettoyage du code
               

03/02/2016
Version 0_4_9: - suppression du code pour le multi asset pour le moment qui pose des soucis a cause des maps
               - suppression du code pour le placement du panel qui semble bugger
               

09/02/2016
Version 1_0_1: - reduction et amelioration du code dans le panel
               - ajout de l'option "active layer" pour choisir si on souhaite importer tout dans le layer actif ou concerver les layers
               - ajout du "clic to import" pour ajouter l'asset actif dans la preview
               

12/02/2016
Version 1_0_2: - ajout du existing_materials qui ne cree pas un nouveau materiau si le nom existe deja
               - ajout du existing_group (idem que existing_material) => a peaufiner
               - ajout du "cancel" en cas de rename dans le panel a l'ajout d'un objet
               - rangement du module property.py
               - ajout du popup des options appele depuis le panel

'''