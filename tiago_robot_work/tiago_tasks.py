from time import sleep
from pycram.worlds.bullet_world import BulletWorld
from pycram.designators.action_designator import *
from pycram.designators.location_designator import *
from pycram.designators.object_designator import *
from pycram.datastructures.enums import ObjectType, WorldMode
from pycram.datastructures.pose import Pose
from pycram.process_module import simulated_robot
from pycram.world_concepts.world_object import Object


#creating the world
world=BulletWorld(WorldMode.GUI)

#adding the kitchen to the world
kitchen=Object('kitchen',ObjectType.ENVIRONMENT,'kitchen.urdf')


#adding the robot to the world
tiago=Object('tiago',ObjectType.ROBOT,'tiago_dual.urdf')
#pr2=Object('pr2',ObjectType.ROBOT,'pr2.urdf')

#add objects to the world
milk=Object('milk',ObjectType.MILK,'milk.stl',pose=Pose([1.3, 1, 0.93]))
#jeroen_cup=Object('jeroen_cup',ObjectType.SPOON,'jeroen_cup.stl',pose=Pose([1.3, 0.8, 0.86]))

#moving to a position
pose1=Pose([0.7, 1, 0])
pose2=Pose([-2,0.9,0])
#nav_description=NavigateAction(target_locations=[pose1])
#nav_designator=nav_description.resolve()


#picking pose
pick_pose = Pose([1.3, 0.9, 0.9])

#moving the torso
mv_torso_descrip=MoveTorsoAction([0.1])
mv_torso_desig=mv_torso_descrip.resolve()


#setting grippers
gripper_right=Arms.RIGHT
gripper_left=Arms.LEFT
motion=GripperState.OPEN
open_right_arm=SetGripperAction(grippers=[gripper_right],motions=[motion]).resolve()
open_left_arm=SetGripperAction(grippers=[gripper_left],motions=[motion]).resolve()


#parking arms
park_right_arm=ParkArmsAction([Arms.RIGHT]).resolve()
park_left_arm=ParkArmsAction([Arms.LEFT]).resolve()
#park_both_arms=ParkArmsAction([Arms.BOTH]).resolve()


milk_desig=BelieveObject(names=["milk"])
jeroen_cup_desig=BelieveObject(names=["jeroen_cup"])

#getting the position of the target objects
target_milk=milk.get_pose()

#target_jeroen_cup=jeroen_cup.get_pose()




with simulated_robot:

    park_right_arm.perform()
    sleep(1)

    park_left_arm.perform()
    sleep(1)

    #navigating to the location and looking at objects
    NavigateAction(target_locations=[pose1]).resolve().perform()
    sleep(1)
    LookAtAction(targets=[target_milk]).resolve().perform()
    sleep(3)

    #pick up objects
    PickUpAction(object_designator_description=milk_desig,
                 arms=[Arms.RIGHT],
                 grasps=[Grasp.RIGHT]).resolve().perform()
    NavigateAction([Pose([-1.90, 0.78, 0.0],
                         [0.0, 0.0, 0.16439898301071468, 0.9863939245479175])]).resolve().perform()

    PlaceAction(object_designator_description=milk_desig,target_locations=[Pose([-1.20, 1.0192, 0.9624],
                                                        [0, 0, 0, 1])],arms=[Arms.RIGHT]).resolve().perform()
    park_right_arm.perform()










