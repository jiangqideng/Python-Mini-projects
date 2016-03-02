# template for "Stopwatch: The Game"

import simplegui 

# define global variables
value = 0
x = 0
y = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t/600
    D = t%10
    C = (t/10)%10
    B = (t-A*600)/100
    return str(A)+':'+str(B)+str(C)+':'+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    if timer.is_running():
        timer.stop()
        global x, y, value
        y += 1
        if value%10 == 0:
            x +=1
    
def reset_handler():
    timer.stop()
    global x, y, value
    value = 0
    x = 0
    y = 0
    print value
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global value
    value += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(value), (40, 90), 40, 'white')
    canvas.draw_text(str(x)+'/'+str(y), (140, 30), 20, 'red')
    
# create frame
frame = simplegui.create_frame('stopwatch', 200, 124)
frame.set_draw_handler(draw_handler)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
start_button = frame.add_button('Start', start_handler, 100)
stop_button = frame.add_button('Stop', stop_handler, 100)
reset_button = frame.add_button('Reset', reset_handler, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
