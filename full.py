#I/usr/bin/env python3
import ev3dev.ev3 as motor
import ev3dev
import time
import math
import regul
import lab_4_classes as odo
from infos import *
###################################################################################################

###################################################################################################
motor_l = motor.LargeMotor(motor.OUTPUT_A)
motor_r = motor.LargeMotor(motor.OUTPUT_D)
startTime = time.time()
prevPos_l = motor_l.position
prevPos_r = motor_r.position
odometry = odo.Odometry(r=wheel_radius, B=base, T=T)
filename="py_coord_one_direction.txt"
f = open(filename, "w")
try:
    while (True):
        t1 = time.time()
        currentTime = time.time() - startTime
        pose_l = motor_l.position - prevPos_l
        pose_r = motor_r.position - prevPos_r

        w_l = motor_l.speed * math.pi / 180
        w_r = motor_r.speed * math.pi / 180
        motor_r.speed

        odometry.update(w_l, w_r)
        rho, alpha = regul.get_error(x_goal, y_goal, odometry.x_integrator.integral, odometry.y_integrator.integral, odometry.theta_integrator.integral)
        alpha=regul.func(alpha)
        v_goal, w_goal = regul.calc_control(rho, alpha)
        #print("v_goal: "+str(v_goal)+" w_goal: "+str(w_goal)+" rho: "+str(rho) + " alpha "+str(alpha))
        ur = regul.saturation(v_goal + w_goal)
        ul = regul.saturation(v_goal - w_goal)
        #print(ur, ul)
        motor_r.run_direct(duty_cycle_sp = ur)
        motor_l.run_direct(duty_cycle_sp = ul)
        x_c, y_c, _ = odometry.update(w_l,w_r)
        print(alpha, x_c, y_c)
        f.write(str(x_c) + " " + str (y_c) +  "\n")
        if rho < 0.2:
            # k+=1
            # x_goal=x_goal*(-1)**(k+1)
            # y_goal=y_goal*(-1)**(k)
            motor_r.run_direct(duty_cycle_sp = 0)
            motor_r.stop(stop_action = 'brake')

            motor_l.run_direct(duty_cycle_sp = 0)
            motor_l.stop(stop_action = 'brake')
            break
            
        
        dt = T - (time.time() - t1)
        if k==6:
            motor_r.run_direct(duty_cycle_sp = 0)
            motor_r.stop(stop_action = 'brake')

            motor_l.run_direct(duty_cycle_sp = 0)
            motor_l.stop(stop_action = 'brake')
            f.close()
            break
        if dt > 0:
            time.sleep(dt)
        else:
            print("TI DAUN")
except:
    motor_r.stop(stop_action = 'brake')
    motor_l.stop(stop_action = 'brake')
