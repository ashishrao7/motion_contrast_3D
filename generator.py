import pattern

def main():

    line = pattern.Line(260, 346, 60, 1)
    line.generate_moving_line('vertical')
    line.generate_moving_line('horizontal')
    #line.generate_moving_line('tl_diag')
    #line.generate_moving_line('bl_diag')
    print('genaration done')


if __name__=='__main__':
    main()