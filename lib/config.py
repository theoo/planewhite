
# server config
host = "10.0.0.1"
port = 4000

# client config
viewport = [(600, 1024), (0, 1024), (0, 1024), (0, 600)]

backgrounds = ["images/bgs/1.jpg", "images/bgs/2.jpg", "images/bgs/3.jpg", "images/bgs/4.jpg"]

#zones_of_interest = [ [],
#                      [ ["images/cut/2_258x574.png", (258, 768 - 574), "This is a wonderful demonstration\n of ten words for carina's sake.", (50,500)] ], 
#                      [ ["images/cut/3_43x766.png", (43, 768 - 766), "Lorem Ipsum", (50,300)], ["images/cut/3_741x396.png", (741, 768 - 396), "arg", (400,600)] ],
#                      [ ["images/cut/4_313x386.png", (313, 768 - 386), "Un intellectuel assis va moins\n loin qu'un con qui marche.", (50,150)] ] ]
                      
zones_of_interest = [ [],
                      [ ["images/cut/2a_187x607.png", (187, 768 - 607), "The curved line is a straight line\n which has been brought out of\n its course by constant sideward pressure.", (150,500)] ], 
                      [ ["images/cut/3a_1x765.png", (1, 768 - 765), "Angular lines originate from the pressure\n of two forces upon a straight line.", (50,300)], ["images/cut/3a_692x447.png", (692, 768 - 447), "The plane becomes a circle when its angles\n multiply in ever increasing numbers\n and become more and more obtuse until\n they finally disappear.", (400,600)] ],
                      [ ["images/cut/4a_269x430.png", (269, 768 - 430), "Four right angles form a square.\n (tentative)", (50,150)] ] ]
                      

CURSOR_IMG_PATH = 'images/cursor.png'
