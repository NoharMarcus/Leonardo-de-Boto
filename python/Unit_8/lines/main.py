import linedraw

lines = linedraw.sketch("images/eiffel.jpg")  # return list of polylines, eg.
# [[(x,y),(x,y),(x,y)],[(x,y),(x,y),...],...]

linedraw.visualize(lines)  # simulates plotter behavior
# draw the lines in order using turtle graphics.


print("")