import pattern

def main():

    #line = pattern.Line(260, 346, 60, 1)
    #line.generate_moving_line('vertical')
    #line.generate_moving_line('horizontal')
    #line.generate_moving_line('tl_diag')
    #line.generate_moving_line('bl_diag')
    wave_image = pattern.wave_2d(260, 346, 30, 10, 1) 
    wave_image.generate_moving_wave('vertical', 'square')
    wave_image.generate_moving_wave('vertical', 'sine')
    #sine_image.generate_moving_sine('horizontal')
    
    print('generation done')


if __name__=='__main__':
    main()