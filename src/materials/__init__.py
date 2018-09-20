pat = ""
folder = pat + "materials"
sub_icons_folder = "icons"
sub_gif_folder = "gifs"
sub_images_folder = "graph"
sub_forms_folder = "forms"

path_to_icons = folder + "//" + sub_icons_folder + "//"
path_to_gifs = folder + "//" + sub_gif_folder + "//"
path_to_images = folder + "//" + sub_images_folder + "//"
path_to_forms = folder + "//" + sub_forms_folder + "//"

class CommonSources():
    # ------ICONS-------
    close_icon = path_to_icons + "Close Window_96px.png"
    # ------GIFS-------
    #------IMAGES-------


#--------------START_MENU--------------
class Start_Menu_Resources(CommonSources):
    # ------FORMS-------
    form = path_to_forms + "start_menu.ui"
    #------GIFS-------
    start_menu_gif = path_to_gifs + "start_menu.gif"
    #------IMAGES-------
    #------ICONS-------




#--------------GAME_WINDOW--------------
class Game_Window_Resources(CommonSources):
    # ------FORMS-------
    form = path_to_forms + "game_window.ui"
    #------GIFS-------
    game_menu_gif = path_to_gifs + "mining.gif"
    #------IMAGES-------
    #------ICONS-------
    multiplayer_icon = path_to_icons + "Multiple Devices_100px.png"
    info_icon = path_to_icons + "Info_100px.png"
    statistic_icon = path_to_icons + "Statistics_100px.png"
    return_icon = path_to_icons + "Return_104px.png"


