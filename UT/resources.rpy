# -*- coding: utf-8 -*-


init: # 1 задание
    python:
        #Трансформы
        def particle_working(trans, st, at):
            """
            Костыльно, но зато просто
            """

            try:
                trans.particle["xmod"] += (.00001 - renpy.random.random()*.00002)
                trans.yalign += trans.particle["speed"]+0.0007
                trans.xalign += trans.particle["xmod"]
                if trans.yalign > 1.1 or trans.xalign > 1.1 or trans.xalign < -0.1:
                    raise
                return .01
            except:
                trans.alpha = .5+(renpy.random.random()/2)
                trans.zoom = .2+(renpy.random.random()/2)
                trans.xalign = renpy.random.random()
                trans.yalign = -.1
                trans.particle = {
                    "xmod": (1 - renpy.random.random()*2)/1000+.0004,
                    "speed": renpy.random.random()/500
                }
                return renpy.random.random()*5


    transform particle_moves():
        alpha 0
        function particle_working
        pause .3
        repeat


    screen snow_falling(count=25):

        text "[count] снежинок одновременно"
        for i in range(count):
            add "UT/particle.png" at particle_moves

init: # 2 и 3

    style menu_label_text:
        font "UT/title.ttf"
        size 45
        color "FFF"

    style menu_button:
        idle_background Solid("666")
        selected_background Solid("A00")
        hover_background Solid("F00")
        xsize 300
        ysize 35

    style menu_text:
        font "UT/buttons.ttf"
        size 35
        color "FFF"

    style menu_slider:
        left_bar Solid("A00")
        hover_left_bar Solid("F33")
        right_bar Solid("666")
        thumb "UT/thumb.jpg"

    style menu_frame:
        background None

    screen preferences():

        tag menu

        use custom_navigation("НАСТРОЙКИ"):
            vbox:

                style_prefix "menu"

                spacing 80

                vbox:
                    spacing 15
                    xfill True

                    hbox:
                        spacing 10
                        add Solid("F00", xsize=5, ysize=50) yalign .5
                        label _("РЕЖИМ ОКНА") yalign .5

                    hbox:
                        spacing 45
                        xalign .5
                        button:
                            text _("ОКОННЫЙ") xalign .5
                            action Preference("display", "window")
                        button:
                            text _("ПОЛНОЭКРАННЫЙ") xalign .5
                            action Preference("display", "fullscreen")

                vbox:
                    spacing 15
                    xfill True

                    hbox:
                        spacing 10
                        add Solid("F00", xsize=5, ysize=50) yalign .5
                        label _("ПРОПУСК") yalign .5

                    hbox:
                        spacing 45
                        xalign .5
                        button:
                            text _("ВСЕГО ТЕКСТА") xalign .5
                            action Preference("skip", "toggle")
                        button:
                            text _("ПОСЛЕ ВЫБОРОВ") xalign .5
                            action Preference("after choices", "toggle")

                vbox:
                    spacing 15
                    xfill True

                    hbox:
                        spacing 10
                        add Solid("F00", xsize=5, ysize=50) yalign .5
                        label _("АУДИО") yalign .5

                    frame:
                        ysize 35
                        bar value Preference("music volume") yalign .5
                        text _("МУЗЫКА") xalign .5

                    frame:
                        ysize 35
                        bar value Preference("sound volume") yalign .5
                        text _("ЗВУКИ") xalign .5


                vbox:
                    spacing 15
                    xfill True

                    hbox:
                        spacing 10
                        add Solid("F00", xsize=5, ysize=50) yalign .5
                        label _("СКОРОСТЬ ТЕКСТА") yalign .5

                    bar value Preference("text speed")



    screen custom_navigation(page_title=""):

        add Solid("CCC")

        frame:
            at transform:
                xalign .5
                on show:
                    xanchor -3.0
                    ease .5 xanchor .5
                on replace:
                    xanchor -3.0
                    ease .5 xanchor .5
            background Solid("333")

            xsize 690
            ysize 1280

            vbox:

                spacing 50
                ypos .005
                xfill True

                frame:
                    xalign .5
                    label page_title text_style "menu_label_text" text_size 70 text_outlines [ (1, "#000A", 2, 2) ] xalign .5
                    background Frame("UT/vbox_underline.png")

                frame:
                    ysize 770
                    xmaximum 680
                    background None
                    transclude

                button:
                    hover_background Solid("F00")
                    idle_background Solid("777")

                    xfill True

                    add "UT/preferences_exit.png" xalign .5

                    action Return()


        use navigation

    screen save_name_modal(accept=NullAction()):
        modal True
        add Solid("#000000") alpha 0.8

        frame:
            padding gui.confirm_frame_borders.padding
            xsize 650
            xalign 0.5
            yalign 0.5

            has vbox:
                xalign 0.5
                spacing 20

            label _("Название сохранения:"):
                text_color gui.text_color
                xalign 0.5

            null height 10

            input size 40 color gui.hover_color default store.save_name changed set_save_name length 15:
                xalign 0.5
                xysize (550, 40)

            textbutton _("Сохранить игру"):
                xalign 0.5
                action [accept, Hide("save_name_modal")]

            key "game_menu" action Hide("save_name_modal")

    style menu_save_button:

        idle_background None
        hover_background Solid("F00")
        ysize 216
        top_padding 0

    screen save():

        tag menu
        use file_slots(_("Сохранить"))

    screen load():

        tag menu
        use file_slots(_("Загрузить"))


    screen file_slots(title):

        default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("A"), quick=_("Q"))

        use custom_navigation(title):

            vbox:
                spacing 10

                for slot in range(1, 4):

                    button:
                        action If(renpy.get_screen("save"), true=Show("save_name_modal", accept=FileSave(slot)), false=FileLoad(slot))
                        style "menu_save_button"
                        add Solid("F00", xsize=15, ysize=216)
                        add Solid("999", xsize=384, ysize=216) xalign .5
                        frame:
                            align (.5, .5)
                            xsize 384
                            ysize 35
                            background Solid("F00")
                            text "Пустой слот" style "menu_text" xalign .5
                        add FileScreenshot(slot) xalign .5

                        if FileSaveName(slot):
                            frame:
                                align (.5, .5)
                                xsize 384
                                ysize 35

                                background Solid("F00")
                                text FileSaveName(slot) style "menu_text" xalign .5


                        if FileLoadable(slot):
                            textbutton "X":
                                text_style "menu_label_text"
                                text_size 70
                                text_idle_color "AAA"
                                text_hover_color "FFF"
                                action FileDelete(slot)
                                yalign .5
                                xalign .95

                hbox:
                    xalign .5


                    hbox:
                        spacing 4

                        button:
                            action FilePage("auto")
                            text _("{#auto_page}A") style "menu_text"
                            selected_background Frame("UT/vbox_underline.png")

                        for page in range(1, 10):

                            button:
                                action FilePage(page)
                                text "[page]" style "menu_text"
                                selected_background Frame("UT/vbox_underline.png")



init -1 python:
    store.save_name = "Новое сохранение"
    def set_save_name(new_name):
        store.save_name = new_name



label start:

    scene image "UT/snow_bg.png"

    show screen snow_falling(100)

    pause

    jump .loop


label .loop:

    window show dissolve
    "Снег падает..."
    "Снежинки"
    window hide dissolve

    pause

    jump .loop
