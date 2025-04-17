#I/usr/bin/env python3
import ev3dev.ev3 as motor
import time

motor_l = motor.LargeMotor(motor.OUTPUT_A)
motor_r = motor.LargeMotor(motor.OUTPUT_A)
startTime = time.time()
startPos_l = motor_l.position
startPos_r = motor_r.position

Kr = 1 #подбираем первым(угол поворота)
Ks = 0 #подбираем вторым

x_goal = 1; y_goal = 1
ks = 1; kr = 1

ro = (1, 0)

while (True):
    currentTime = time.time() - startTime
    pose_l = motor_l.position - startPos_l
    pose_r = motor_r.position - startPos_r

    w_l = motor_l.speed
    w_r = motor_r.speed
    motor_a.run_direct(duty_cycle_sp = vol)
    f.write(str(currentTime) + " " + str(motor_pose) + " " + str (motor_vel) + "\n")
    if currentTime > 1:
        motor_a.run_direct(duty_cycle_sp = 0)
        motor_a.stop(stop_action = 'brake')

        time.sleep(1)
        break