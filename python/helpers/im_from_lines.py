from PIL import Image, ImageDraw

def create_img_from_lines(lines):
    """
    this fucntion creates a visualization of the final drawing
    :param lines: NORMALIZED lines (lines after normalization such that all lines will be within the paper size)
    :return: img - a PIL img of all the lines
    """

    width, height = (297, 210)  # paper size

    # creating new Image object
    img = Image.new('RGB', (width, height), color='white')

    # create line image
    img1 = ImageDraw.Draw(img)

    for line in lines:

        # since normalized lines are centered to the robot coordinates, convert the center of the line paintings to an img coordinates
        # (such that x-axis range is from 0 to 297 and not from -x to x)
        centered_x_axis_line = []
        for coord in line:
            centered_x_axis_line.append((coord[0]+290//2, coord[1]))

        img1.line(centered_x_axis_line, fill="blue", width=0)
    return img

