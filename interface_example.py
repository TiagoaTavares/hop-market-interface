#!/usr/bin/env python3
import pygtk
pygtk.require('2.0')
import gtk
# Create a new window
window = gtk.Window()

# Here we connect the "delete-event" event to a signal handler.
# This event occurs when we the user closes window,
# We connect it to gtk.main_quit, so it quits the main loop
# and the program terminates
window.connect("delete-event", gtk.main_quit)

# Sets the border width of the window.
window.set_border_width(10)

# Creates a new button with the label "Hello World".
button = gtk.Button("Hello World")

# This is a callback function, which we later will connect
# to the clicked signal of the button, which will be triggered
# when the user clicks the button with a mouse.
def on_button_clicked(button):
    print ("Hello World")
# When the button receives the "clicked" signal, it will call the
# function hello() defined above.
button.connect("clicked", on_button_clicked)

# This packs the button into the window (which is a container).
window.add(button)

# Show the window and the button
window.show_all()
# Run the main loop, to process events such a key presses
# and mouse movements.
gtk.main()