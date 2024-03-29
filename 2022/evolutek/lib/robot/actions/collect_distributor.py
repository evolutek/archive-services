from evolutek.lib.robot.robot_actions_imports import *

ArmToPomb = {
    FrontArmsEnum.Right : "1",
    FrontArmsEnum.Center : "2",
    FrontArmsEnum.Left : "3"
}

def reverse_sample(self, x, y, pos, arm): #pos = string : x or y, axe distributor
    ##if sheat happend replace [index] by .Center
    # Step 1
    self.actuators.ax_move(arm.get_head_id(), 550)
    self.actuators.ax_move(arm.get_elevator_id(), 730)
    sleep(1)

    # Grap sample
    self.pumps_get(ids=ArmToPomb[arm], async_task=False)

    # Forward
    self.goto_avoid(x, y, async_task=False)

    # Step 2
    self.actuators.ax_move(arm.get_head_id(), 515)
    self.actuators.ax_move(arm.get_elevator_id(), 815)

    # Backward simultanously with step 2
    speed = self.trajman.get_speeds()['trmax']
    self.trajman.set_trsl_max_speed(10)
    self.goto_avoid((x+100 if pos == "y" else x), (y+100 if pos == "x" else y), async_task=False)
    self.trajman.set_trsl_max_speed(speed)

    # Disable pump
    self.pumps_drop(ids=ArmToPomb[arm], use_ev=False, async_task=False)

    # Continue to backward
    self.set_head_config(arm=arm.get_head_id(), config=HeadConfig.Down, async_task=False)
    sleep(0.2)
    self.goto_avoid((x+125 if pos == "y" else x), (x+125 if pos == "y" else x), async_task=False)


def grab_sample(self, arm):
    #set elevator to down
    self.set_elevator_config(arm=arm, config=ElevatorConfig.Down, async_task=False)
    sleep(0.2)
        #activated pump
    self.pumps_get(ids=ArmToPomb[arm], async_task=False)
    sleep(1)

    self.set_elevator_config(arm=arm, config=ElevatorConfig.Closed, async_task=False)
    self.set_head_config(arm=ArmToPomb[arm], config=HeadConfig.Galery, async_task=False)


def go_galery(self, onY):
    if(onY): #dodge galery
        my_y = self.get_position()["y"] # NOT MIRRORED /!\
        self.goto_avoid(320, my_y, async_task=False, timeout=10)
        self.goth(theta=pi, async_task=False)
    else:
        my_x = self.get_position()["x"] # NOT MIRRORED /!\
        self.goto_avoid(my_x, 320, async_task=False, timeout=10)
        self.goth(theta=-pi/2, async_task=False)
        #go to galery
    self.goto_avoid(320, 810, async_task=False, timeout=10)
    self.goth(theta=pi, async_task=False)
    self.goto_avoid(190, 810, async_task=False, timeout=10)
        #drop into
    self.pumps_drop(ids="1", async_task=False)
    self.pumps_drop(ids="2", async_task=False)
    self.pumps_drop(ids="3", async_task=False)
        #go back
    self.goto_avoid(320, 810, async_task=False, timeout=10)
        #reset arms
    self.set_elevator_config(arm=1, config=ElevatorConfig.Mid, async_task=False)
    self.set_elevator_config(arm=2, config=ElevatorConfig.Mid, async_task=False)
    self.set_elevator_config(arm=3, config=ElevatorConfig.Mid, async_task=False)
    self.set_head_config(arm=1, config=HeadConfig.Down, async_task=False)
    self.set_head_config(arm=2, config=HeadConfig.Down, async_task=False)
    self.set_head_config(arm=3, config=HeadConfig.Down, async_task=False)

@if_enabled
@async_task
def collect_distributor(self, yORx="y"):
    x, y = 0, 0
    if (yORx == "y"):
        x = 1250#-15 ##test 16
        y = 270
    elif (yORx == "x"):
        x = 270
        y = 1350#+15 ##test 16
    else:
        print("Mistake in parametre: choose 'x' or 'y' ")

    self.goto_avoid(x, y, async_task=False)
    self.goth(-pi/2, async_task=False)
    reverse_sample(self, x, y, yORx, FrontArmsEnum.Right)
    ##offset
    grab_sample(self, FrontArmsEnum.Right)
    ##if up ok , test down
    """
    if (yORx == "y"):
        x += 5
        y -= 2 ##or 1.5 if can
    else:
        x -= 2 ##or 1.5
        y -= 5
    self.goto_avoid(x, y, async_task=False)
    self.goth(-pi/2, async_task=False)
    get_sample(self, x, y, yORx, 2)
    grab_palets(2)
    if (yORx == "y"):
        x += 10
        y -= 2 ##or 1.5 if can
    else:
        x -= 2 ##or 1.5
        y -= 10
    self.goto_avoid(x, y, async_task=False)
    self.goth(-pi/2, async_task=False)
    get_sample(self, x, y, yORx, 3)
    grab_palets(3)

    """
    return RobotStatus.return_status(RobotStatus.Done,score=9)












"""
Step 1:
3 : 550
4 : 730

Step 2:
3 : 512
4 : 815


"""