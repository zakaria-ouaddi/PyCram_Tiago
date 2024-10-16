from pycram.worlds.bullet_world import BulletWorld
from pycram.world_concepts.world_object import Object
from pycram.process_module import simulated_robot, with_simulated_robot
from pycram.designators.motion_designator import *
from pycram.designators.location_designator import *
from pycram.designators.action_designator import *
from pycram.designators.object_designator import *
from pycram.datastructures.enums import ObjectType, Arms, Grasp, WorldMode
from pycram.designators.motion_designator import *


#creating the world
world=BulletWorld(WorldMode.GUI)


#adding the kitchen to the world
kitchen=Object('kitchen',ObjectType.ENVIRONMENT,'kitchen.urdf')


#adding the robot to the world
pr2=Object('pr2',ObjectType.ROBOT,'pr2.urdf')


#add objects to the world
milk=Object('milk',ObjectType.MILK,'milk.stl',pose=Pose([1.3, 1, 0.94]))
spoon=Object('spoon',ObjectType.SPOON,'spoon.stl',pose=Pose([1.3, 1.2, 0.86]))
breakfast_cereal=Object('jeroen_cup',ObjectType.BREAKFAST_CEREAL,'breakfast_cereal.stl',pose=Pose([1.3, 0.5, 0.97]))
bowl=Object('bowl',ObjectType.BOWL,'bowl.stl',pose=Pose([1.3, 0.8, 0.89]))



#finding poses
def find_pose(trgt,rbt):
    target=BelieveObject(types=[trgt]).resolve()
    robot=BelieveObject(types=[rbt]).resolve()
    ps=CostmapLocation(target=target,reachable_for=robot).resolve()
    return ps.pose



@with_simulated_robot
def nav_and_det(trgt,rbt,trgtname):
    NavigateAction([find_pose(trgt,rbt)]).resolve().perform()
    LookAtAction(targets=[trgtname.get_pose()]).resolve().perform()
    object_desig=DetectAction(BelieveObject(types=[trgt])).resolve().perform()
    return  object_desig


@with_simulated_robot
def find_and_place(trgt,randnbr):
    kitchen_desig = BelieveObject(names=["kitchen"]).resolve()
    location_description = SemanticCostmapLocation(urdf_link_name="kitchen_island_surface",part_of=kitchen_desig,for_object=trgt)
    ps = [p.pose for p in location_description]
    TransportAction(trgt, [Arms.RIGHT], [ps[randnbr]]).resolve().perform()



with simulated_robot:
    MoveTorsoAction([0.3]).resolve().perform()
    ParkArmsAction([Arms.BOTH]).resolve().perform()

    #transportation using SemanticCostmapLocation

    #transporting milk
    milk_trprt=nav_and_det(ObjectType.MILK,ObjectType.ROBOT,milk)
    find_and_place(milk_trprt,4)

    # transporting spoon
    spoon_trprt = nav_and_det(ObjectType.SPOON, ObjectType.ROBOT, spoon)
    find_and_place(spoon_trprt,18)

    # transporting bowl
    bowl_trprt = nav_and_det(ObjectType.BOWL, ObjectType.ROBOT, bowl)
    find_and_place(bowl_trprt, 6)

    # transportation breakfast_cereal using given position
    breakfast_cereal_trprt = nav_and_det(ObjectType.BREAKFAST_CEREAL, ObjectType.ROBOT, breakfast_cereal)
    TransportAction(breakfast_cereal_trprt, [Arms.RIGHT], [Pose([-1.30, 1.6, 0.95])]).resolve().perform()
