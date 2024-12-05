import time
from pycram.worlds.bullet_world import BulletWorld
from pycram.designators.action_designator import *
from pycram.designators.location_designator import *
from pycram.designators.object_designator import *
from pycram.datastructures.enums import *
from pycram.datastructures.pose import Pose
from pycram.process_module import simulated_robot, with_simulated_robot
from pycram.world_concepts.world_object import Object
from pycram.datastructures.world import World

world=BulletWorld(WorldMode.GUI)

apartment=Object('apartment',ObjectType.ENVIRONMENT,'apartment.urdf')

stretch=Object('stretch',ObjectType.ROBOT,'stretch_description.urdf',pose=Pose([2.2, 2.5, 0]))

#adding objects that will be inside drawers
#spoon=Object('spoon',ObjectType.SPOON,'spoon.stl',pose=Pose([2.4, 2.2, 0.68]))
milk=Object('milk',ObjectType.MILK,'milk.stl',pose=Pose([0.5, 2.525,1.15]))
#bowl=Object('bowl',ObjectType.BOWL,'bowl.stl',pose=Pose([2.4, 2.2, 1]))
jeroen_cup=Object('jeroen_cup',ObjectType.JEROEN_CUP,'jeroen_cup.stl',pose=Pose([0.445, 3.01, 0.58]))

#adding inside drawer
#apartment.attach(spoon, 'cabinet10_drawer_middle')
apartment.attach(jeroen_cup, 'cabinet5_drawer_middle')
apartment.attach(milk, 'cabinet3')

#BelieveObject: Description for Objects that are only believed in
robot_desig = BelieveObject(names=["stretch"])
apartment_desig = BelieveObject(names=["apartment"])
milk_desig = BelieveObject(names=["milk"])

#we suppose that the fridge is slightly opened using blum api
apartment.set_joint_position('cabinet3_door_top_left_joint', 0.08)

'''
In this demo, the robot primarily moves its joints to reach and pick up an object.
Once the object is grasped, the attach method is used to secure it to the robot's arm.
The robot then transports the object to a specified position and detaches it from the arm.

'''


#opening fridge
@with_simulated_robot
def open_fridge():
    MoveTorsoAction([0.9]).resolve().perform()
    NavigateAction([Pose([1.16,3.2,0],[0,0,-1,1])]).resolve().perform()
    LookAtAction([Pose([0.5, 2.5,1.3])]).resolve().perform()
    if apartment.get_joint_position('cabinet3_door_top_left_joint') >= 0.08:
        MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0.1, 0.1, 0.1, 0.1, 0.1]).perform()
        time.sleep(2)
        MoveJointsMotion(['joint_wrist_yaw'], [1.5]).perform()
        time.sleep(2)
        MoveJointsMotion(['joint_wrist_roll'], [1.5]).perform()
        time.sleep(2)
        NavigateAction([Pose([1.16,2.95,0],[0,0,-1,1])]).resolve().perform()
        time.sleep(2)
        MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                         [0.08, 0.08, 0.05, 0.05, 0.05]).perform()
        apartment.set_joint_position('cabinet3_door_top_left_joint', 0.3)
        time.sleep(2)
        NavigateAction([Pose([1.3,2.45,0],[0,0,-1,1])]).resolve().perform()
        apartment.set_joint_position('cabinet3_door_top_left_joint', 1.5)

    else:
        print('cannot open')

#detecting milk inside fridge and transport it
@with_simulated_robot
def milk_transporting():
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0, 0, 0, 0, 0]).perform()
    NavigateAction([Pose([1.14,2.5,0],[0,0,-1,1])]).resolve().perform()
    LookAtAction([milk.pose]).resolve().perform()
    MoveTorsoAction([1]).resolve().perform()
    #work on detection ...


    #grabing milk from fridge
    MoveJointsMotion(['joint_wrist_yaw'], [0]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_roll'], [0]).perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.OPEN]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0.05, 0.05, 0.08, 0.08, 0.8]).perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT],[GripperState.CLOSE]).resolve().perform()
    apartment.detach(milk)
    stretch.attach(milk,'link_straight_gripper')
    NavigateAction([Pose([2.2, 2.8, 0])]).resolve().perform()

    #putting milk down
    LookAtAction([Pose([2.4,2.5,1])]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_yaw'], [1.5]).perform()
    time.sleep(2)
    MoveTorsoAction([0.88]).resolve().perform()
    stretch.detach(milk)
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.OPEN]).resolve().perform()
    time.sleep(2)
    NavigateAction([Pose([1.8, 2.8, 0])]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_yaw'], [0]).perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.CLOSE]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0, 0, 0, 0, 0]).perform()

#opening drawer
@with_simulated_robot
def open_drawer():
    NavigateAction([Pose([1.35,3.05,0],[0,0,-1,1])]).resolve().perform()
    time.sleep(2)
    LookAtAction([jeroen_cup.pose]).resolve().perform()
    time.sleep(2)
    MoveTorsoAction([0.614]).resolve().perform()
   # time.sleep(2)
   # MoveJointsMotion(['joint_wrist_yaw'], [0]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_roll'], [1.5]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3','joint_arm_l4'],[0.1,0.1,0.1,0.03,0.04]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_gripper_finger_right','joint_gripper_finger_left'],[-0.1,-0.1]).perform()
    time.sleep(2)
    apartment.set_joint_position('cabinet5_drawer_middle_joint', 0.3)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                    [0, 0, 0, 0.03, 0.04]).perform()

@with_simulated_robot
def transport_cup():
    SetGripperAction([Arms.RIGHT], [GripperState.OPEN]).resolve().perform()
    LookAtAction([jeroen_cup.pose]).resolve().perform()
    time.sleep(2)
    MoveTorsoAction([1]).resolve().perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.CLOSE]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_roll'], [0]).perform()
    #time.sleep(2)
    MoveJointsMotion(['joint_wrist_yaw'], [1.5]).perform()
    NavigateAction([Pose([0.93,3.22,0],[0,0,1,-1])]).resolve().perform()
    time.sleep(2)
    LookAtAction([jeroen_cup.pose]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_gripper_finger_left','joint_gripper_finger_right'],[0.25,0.25]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_pitch'],[-0.2]).perform()
    time.sleep(2)
    MoveTorsoAction([0.62]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_gripper_finger_left', 'joint_gripper_finger_right'], [0.06, 0.06]).perform()
    time.sleep(2)
    apartment.detach(jeroen_cup)
    stretch.attach(jeroen_cup,'link_gripper_finger_right')
    MoveTorsoAction([1]).resolve().perform()
    time.sleep(2)
    NavigateAction([Pose([1.9,2,0],[0,0,1,1])]).resolve().perform()
    time.sleep(2)
    LookAtAction([Pose([2.5,2.2,1])]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0.1, 0.1, 0.1, 0.1, 0.1]).perform()
    time.sleep(2)
    stretch.detach(jeroen_cup)
    SetGripperAction([Arms.RIGHT],[GripperState.OPEN]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_pitch'], [0]).perform()
    time.sleep(2)
    NavigateAction([Pose([1.9, 1.8, 0], [0, 0, 1, 1])]).resolve().perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.CLOSE]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_wrist_yaw'], [0]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0, 0, 0, 0, 0]).perform()

@with_simulated_robot
def close_fridge():
    NavigateAction([Pose([0.9, 1.7, 0], [0, 0, -1, 0])]).resolve().perform()
    LookAtAction([Pose([1,3,1])]).resolve().perform()
    time.sleep(2)
    MoveTorsoAction([1]).resolve().perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0.1, 0.1, 0.1, 0.1, 0.1]).perform()
    apartment.set_joint_position('cabinet3_door_top_left_joint', 0)
    ParkArmsAction([Arms.RIGHT]).resolve().perform()


    #current_pos=apartment.get_joint_position('cabinet3_door_top_left_joint')
    #while current_pos>0:
     #   current_pos-=0.1
       # apartment.set_joint_position('cabinet3_door_top_left_joint', current_pos)

@with_simulated_robot
def close_drawer():
    MoveTorsoAction([0.614]).resolve().perform()
    NavigateAction([Pose([1.35,3.05,0],[0,0,-1,1])]).resolve().perform()
    MoveJointsMotion(['joint_wrist_roll'], [1.5]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_gripper_finger_left', 'joint_gripper_finger_right'], [0.1, 0.1]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0, 0, 0, 0.03, 0.04]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_gripper_finger_left', 'joint_gripper_finger_right'], [-0.1,-0.1]).perform()
    time.sleep(2)
    MoveJointsMotion(['joint_arm_l0', 'joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3', 'joint_arm_l4'],
                     [0.1, 0.1, 0.1, 0.03, 0.04]).perform()
    apartment.set_joint_position('cabinet5_drawer_middle_joint', 0)
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.OPEN]).resolve().perform()
    time.sleep(2)
    NavigateAction([Pose([1.4,3.05,0],[0,0,-1,1])]).resolve().perform()
    time.sleep(2)
    SetGripperAction([Arms.RIGHT], [GripperState.CLOSE]).resolve().perform()
    NavigateAction([Pose([1.5,2.2,0])]).resolve().perform()
    time.sleep(2)
    ParkArmsAction([Arms.RIGHT]).resolve().perform()

#print(stretch.get_joint_limits('joint_arm_l0'))
with simulated_robot:
    open_fridge()
    milk_transporting()
    close_fridge()
    open_drawer()
    transport_cup()
    close_drawer()



