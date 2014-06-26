import numpy, pygame

def AACircle(radius, antialias=2, color=[255, 128, 0], width=0, surface=None):
    ' Paint a circle'
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    d = radius * 2
    r2 = radius * antialias
    d2 = r2 * 2

    # Create surface twice the size (or more)
    pic = pygame.Surface([d2, d2], 0, 8)
    pic.set_palette([[x, x, x] for x in range(256)])
    pic.fill(BLACK)

    # Draw the circle on the large picture
    pygame.draw.circle(pic, WHITE, [r2, r2], r2, width)

    # Add the pixel values to a temporary array
    if not surface:
        surface = pygame.Surface([d, d], pygame.SRCALPHA, 32)
    surface.fill(color)
    array = numpy.zeros((d, d), numpy.int)
    srcarray = pygame.surfarray.pixels2d(pic)
    for x in range(d2):
        for y in range(d2):
            array[x / antialias, y / antialias] += srcarray[x][y]
    array /= antialias * antialias

    # Create the final surface
    pygame.surfarray.pixels_alpha(surface)[:, :] = array.astype(numpy.int8)

    # Return the final surface
    return surface

