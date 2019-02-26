import pattern

def main():

    #line = pattern.Line(260, 346, 60, 1)
    #line.generate_moving_line('vertical')
    #line.generate_moving_line('horizontal')
    #line.generate_moving_line('tl_diag')
    #line.generate_moving_line('bl_diag')
    sine_image = pattern.sinusoid_2d(260, 346, 120, 250, 1) 
    sine_image.generate_moving_sine('vertical')
    #sine_image.generate_moving_sine('horizontal')
    
    print('generation done')


if __name__=='__main__':
    main()