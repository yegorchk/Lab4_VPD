#I/usr/bin/env python3
import ev3dev.ev3 as motor
import ev3dev
import time
import math
import regul
from infos import *
import lab_4_classes as odo

motor_l = motor.LargeMotor(motor.OUTPUT_A)
motor_r = motor.LargeMotor(motor.OUTPUT_D)
startTime = time.time()
prevPos_l = motor_l.position
prevPos_r = motor_r.position

odometry = odo.Odometry(r=wheel_radius, B=base, T=T)

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
        v_goal, w_goal = regul.calc_control(rho, alpha)
        print("v_goal: "+str(v_goal)+" w_goal: "+str(w_goal)+" rho: "+str(rho) + " alpha "+str(alpha))
        ur = regul.saturation(v_goal + w_goal)
        ul = regul.saturation(v_goal - w_goal)
        #print(ur, ul)

        motor_r.run_direct(duty_cycle_sp = ur)
        motor_l.run_direct(duty_cycle_sp = ul)
        
        #f.write(str(currentTime) + " " + str(motor_pose) + " " + str (motor_vel) + "\n")
        if rho < 0.05:
            motor_r.run_direct(duty_cycle_sp = 0)
            motor_r.stop(stop_action = 'brake')

            motor_l.run_direct(duty_cycle_sp = 0)
            motor_l.stop(stop_action = 'brake')
        
        dt = T - (time.time() - t1)
    
        #     #motor_a.run_direct(duty_cycle_sp = 0)
        #     #motor_a.stop(stop_action = 'brake')
        if dt > 0:
            time.sleep(dt)
        else:
            print("TI DAUN")
except:
    motor_r.stop(stop_action = 'brake')
    motor_l.stop(stop_action = 'brake')
