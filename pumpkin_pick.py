import turtle


wn = turtle.Screen()
wn.title("Pumpkin Picker")

wn.setup(width = 560, height = 350)
bg_image = "background.png"
wn.bgpic(bg_image)

wn.addshape("pumpkin.png", shape="image")
turtle.shape("gfg.gif")

wn.mainloop()   