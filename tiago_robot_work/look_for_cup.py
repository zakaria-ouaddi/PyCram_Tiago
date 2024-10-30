from pycram.worlds.bullet_world import BulletWorld
from pycram.world_concepts.world_object import Object
from pycram.process_module import simulated_robot, with_simulated_robot
from pycram.designators.location_designator import *
from pycram.designators.action_designator import *
from pycram.designators.object_designator import *
from pycram.datastructures.enums import Grasp, WorldMode
from pycram.designators.motion_designator import *

#creating the world
world=BulletWorld(WorldMode.GUI)

#adding the apartment and the pr2 robot
apartment=Object('apartment',ObjectType.ENVIRONMENT,'apartment.urdf')
pr2=Object('pr2',ObjectType.ROBOT,'pr2.urdf',pose=Pose([1.2,2,0]))

#adding the object milk
milk=Object('milk',ObjectType.MILK,'milk.stl',pose=Pose([2.4, 2.2,1]))

#adding objects that will be inside drawers
bowl=Object('bowl',ObjectType.BOWL,'bowl.stl',pose=Pose([2.4, 2.2, 0.68]))
spoon=Object('spoon',ObjectType.SPOON,'spoon.stl',pose=Pose([2.5, 2.3, 0.86]))
jeroen_cup=Object('jeroen_cup',ObjectType.JEROEN_CUP,'jeroen_cup.stl',pose=Pose([0.5, 3, 0.58]))

#adding objects to drawers
apartment.attach(spoon, 'cabinet10_drawer_top')
apartment.attach(bowl, 'cabinet10_drawer_middle')
apartment.attach(jeroen_cup, 'cabinet5_drawer_middle')

#the position where the robot going to look to pick up the milk object
pick_pose = Pose([2.4, 2.15, 1])

#BelieveObject: Description for Objects that are only believed in
robot_desig = BelieveObject(names=["pr2"])
apartment_desig = BelieveObject(names=["apartment"])


@with_simulated_robot
def move_and_detect(obj_type):
    NavigateAction(target_locations=[Pose([1.7, 2, 0])]).resolve().perform()

    LookAtAction(targets=[pick_pose]).resolve().perform()

    object_desig = DetectAction(BelieveObject(types=[obj_type])).resolve().perform()

    return object_desig


@with_simulated_robot
def transport_obj(obj,obj_typ,handle_name,target_pose):

    handle_desig = ObjectPart(names=[handle_name], part_of=apartment_desig.resolve())
    drawer_open_loc = AccessingLocation(handle_desig=handle_desig.resolve(),robot_desig=robot_desig.resolve()).resolve()

    NavigateAction([drawer_open_loc.pose]).resolve().perform()

    OpenAction(object_designator_description=handle_desig, arms=[drawer_open_loc.arms[0]]).resolve().perform()
    obj.detach(apartment)

    LookAtAction([apartment.get_link_pose(handle_name)]).resolve().perform()

    obj_desig = DetectAction(BelieveObject(types=[obj_typ])).resolve().perform()

    pickup_arm = Arms.LEFT if drawer_open_loc.arms[0] == Arms.RIGHT else Arms.RIGHT
    PickUpAction(obj_desig, [pickup_arm], [Grasp.TOP]).resolve().perform()

    ParkArmsAction([Arms.LEFT if pickup_arm == Arms.LEFT else Arms.RIGHT]).resolve().perform()

    CloseAction(object_designator_description=handle_desig, arms=[drawer_open_loc.arms[0]]).resolve().perform()

    ParkArmsAction([Arms.BOTH]).resolve().perform()

    placing_loc = CostmapLocation(target=target_pose, reachable_for=robot_desig.resolve()).resolve()
    NavigateAction([placing_loc.pose]).resolve().perform()

    PlaceAction(obj_desig, [target_pose], [pickup_arm]).resolve().perform()

#positions for the transporting
spoon_pose=Pose([4.85, 3.3, 0.73])
bowl_pose=Pose([2.4, 2.2,0.99])
jeroen_cup_pose=Pose([2.4, 2.5,0.95])


with simulated_robot:
    ParkArmsAction([Arms.BOTH]).resolve().perform()

    MoveTorsoAction([0.35]).resolve().perform()

    #detect milk and transport it
    milk_desig=move_and_detect(ObjectType.MILK)
    TransportAction(milk_desig,[Arms.RIGHT],[Pose([4.8, 3.55, 0.8])]).resolve().perform()

    #looking for the three objects and transporting them to the giving position
    transport_obj(spoon,ObjectType.SPOON,"handle_cab10_t",spoon_pose)
    transport_obj(bowl,ObjectType.BOWL,"handle_cab10_m",bowl_pose)
    transport_obj(jeroen_cup,ObjectType.JEROEN_CUP,"handle_cab5_m",jeroen_cup_pose)

    MoveTorsoAction([0.2]).resolve().perform()
    ParkArmsAction([Arms.BOTH]).resolve().perform()

