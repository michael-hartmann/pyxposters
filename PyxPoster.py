from pyx import canvas, color, deformer, document, epsfile, path, style, text, trafo, unit

class Poster:
    """Creation of posters in Pyx

    The poster consists of a title bar, a background and boxes. The title bar
    containt the title of the poster, a logo, and the authors. The background
    is typically just a color or an image. The main part of the poster consists
    of boxes. At the moment the layout just supports two columns.

    A box has a title and content. The user gives a Pyx canvas and a title
    (string), and the method add_box will make a box out of it with correct
    size.
    """
    def __init__(self, title, authors, latex_headers, width=840*unit.t_mm, height=1200*unit.t_mm, titleheight=100*unit.t_mm):
        """Create a new Pyx poster"""
        self.width = width
        self.height = height
        self.titleheight = titleheight
        self.title = title
        self.authors = authors

        self.ygap = unit.t_cm # gap in y between two boxes

        self.mntfcolor = color.hsb(178./360, 1, 0.4)

        # initialize pyx
        text.set(text.LatexRunner, texenc="utf8")
        text.preamble(latex_headers)
        unit.set(xscale=4, wscale=4, vscale=4)

        c = self.c = canvas.canvas()

        # title, authors, logo
        c.fill(path.rect(0, height-titleheight, width, titleheight), [self.mntfcolor])
        c.text(24*unit.t_mm, height-55*unit.t_mm, title,   [color.grey(1)])
        c.text(25*unit.t_mm, height-88*unit.t_mm, authors, [color.grey(1)])
        c.insert(epsfile.epsfile(width-145*unit.t_mm, height-88*unit.t_mm, "images/Uni_Aug_Logo_Basis_neg_C.eps"))

        # background
        top = height-titleheight-3*unit.t_mm
        c.fill(path.rect(0, 0, width, top), [color.grey(0.8)])

        # left and right y
        self.y_left  = 1*unit.t_cm
        self.y_right = 1*unit.t_cm


    def add_box(self, canvas, col, title, bbox=False):
        """Add a box at column (left or right) with title. The origin of the
        canvas must be (0,0)"""
        c = self.c
        titleheight = self.titleheight
        width, height = self.width, self.height

        x = 0.02*width
        if col.lower() == "left":
            y = height-titleheight-3*unit.t_mm- self.y_left
        else: # right
            x = 0.5*width+0.5*x
            y = height-titleheight-3*unit.t_mm- self.y_right

        canvas_height = canvas.bbox().height()
        ht = canvas_height + 7*unit.t_cm

        shift = trafo.translate(x, y-ht)
        c.fill(path.rect(0, 0, 0.47*width, ht),
               [deformer.smoothed(radius=3*unit.t_cm),
                color.grey(1), shift])

        shift = trafo.translate(x, y)
        c.text(1.5*unit.t_cm, -3*unit.t_cm, r'\large\bfseries %s' % title, [self.mntfcolor, shift])

        shift = [trafo.translate(
            x-canvas.bbox().left()+0.5*(0.47*width-canvas.bbox().width()),
            y-ht - canvas.bbox().bottom() + 1*unit.t_cm
        )]

        if bbox:
            c.stroke(canvas.bbox().rect(), shift)

        c.insert(canvas, shift)

        if col.lower() == "left":
            self.y_left += ht + self.ygap
        else:
            self.y_right += ht + self.ygap


    def get_canvas(self):
        """Get canvas of total poster"""
        return self.c


    def print_grid(self):
        """Print a grid on the poster. This might be helpful for debugging"""
        for nx in range(0,84,5):
            self.c.stroke(path.line(nx,0,nx,self.height), [style.linestyle.dashed])
        for ny in range(0,120,5):
            self.c.stroke(path.line(0,ny,self.width,ny), [style.linestyle.dashed])


    def writeEPSfile(self):
        d = document.page(self.c, paperformat=document.paperformat.A0)
        document.document(pages=[d]).writeEPSfile()


    def writePDFfile(self):
        d = document.page(self.c, paperformat=document.paperformat.A0)
        document.document(pages=[d]).writePDFfile()


    def latex2canvas(self,latex):
        """Return a canvas out of LaTeX text. The code will generate a minipage
        and convert the minipage to a PyX canvas"""
        c = canvas.canvas()
        start = r"\begin{minipage}{9.2truecm}" + "\n"
        end   = r"\end{minipage}"
        c.insert(text.text(0,0, start + latex + end))
        return c
