import pygame
from multineuro.forms.input import Input
from multineuro.forms.forms import Form
def main():
    # Run example
    pygame.init()
    screen = pygame.display.set_mode((400, 300)) # Create form
    f = Form(True) # Add objects
#    f.add_object('text', Text('I am some text', label_style=['bold', 'underline']))
    f.add_object('Name', Input('Nombre', '',
                                label_size=18,
                                input_border_color=(255, 100, 100),
                                input_border_width=0,
                                input_bg_color=(0, 0, 0, 0)))
#    f.add_object('Name', Input('More Input:', 'More testing'))#, position='absolute', top=100, left=20))
#    sel = Select(border_width=2, top=50)
#    sel.add_option('option1', 1)
#    sel.add_option('option2', 2)
#    sel.add_option('option3 which is really long', 3)
#    sel.add_option('option4', 4)
#    sel.add_option('option5', 5)
#    sel.add_option('option6', 6)
#    f.add_object('select', sel)
#    f.add_object('submit', Button('Submit', f.submit, ()))
#    f.add_object('reset', Button('Reset', f.clear, ()))
#    f.rem_object('Name')
# Run form
    r = f.run(screen)
    # Display results
    for kv in r.iteritems():
        print '%s:\t%s' % kv # End

    pygame.quit()



if __name__ == '__main__':
    main()
