from simplepygamemenus.menu import Menu

# THESE IMPORTS ARE NECCESSARY
import sys
import os
import pygame

"""
SIMPLE PYGAME MENUS
    By Leonardo Ferrisi: ferrisil@union.edu

--------------------------------------------

Use this package to create simple menus for your pygame games!
--------------------------------------------------------------

How to use:

Create a main menu using the 'Menu()' construtor

    Example:
        myMenu = Menu(title="MyMainMenu")

Add buttons using:

        myMenu.add_button(label='button text', x, y, fontsize, function=<function to perform>)

        Example:
            if you have added a second menu, you can switch to it using your new button using the:
                
                `menuName.run_menu` function

        Example2:

            myMenu = Menu(title="MyMainMenu")
            myOtherMenu = Menu(title="myOtherMenu")
            myMenu.add_button(label='button text', x, y, fontsize, function=myOtherMenu.run_main)

    I'll add more soon, see the example below!

"""
if __name__ == "__main__":
    main = Menu()
    main.add_text(text="TEST", x=250, y=20, size=30)
    b_menu = Menu(main=main, title="other menu", showESCKEYhint=True)
    main.add_button(label="go to next", x=250, y=250, fontsize=30, function=b_menu.run_menu)
    b_menu.add_button(label="exit", x=250, y=250, fontsize=30, function=sys.exit)

    next_menu = Menu(title="NEXT",main=b_menu)
    b_menu.add_button(label="next menu", x=250, y=400, fontsize=30, basecolor=(0,255,0), hovercolor=(255,255,255), function=next_menu.run_menu)

    main.run_menu()

