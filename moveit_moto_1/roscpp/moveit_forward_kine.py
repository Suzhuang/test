#!/usr/bin/python

import roslib; roslib.load_manifest('motoman_driver')
import rospy
import sensor_msgs.msg
import moveit_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import copy
import rospy,sys
import moveit_commander
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import PlanningScene, ObjectColor
from geometry_msgs.msg import PoseStamped, Pose 

class MoveItDemo:
	def setColor(self,name,r,g,b,a=0.9):
			color=ObjectColor()
			color.id=name
			color.color.r=r
			color.color.g=g
			color.color.b=b
			color.color.a=a
			self.colors[name]=color
		    
	def sendColors(self):
			p=PlanningScene()
			p.is_diff=True
			for color in self.colors.values():
				p.object_colors.append(color)
			self.scene_pub.publish(p)	
			
	def __init__(self):
		#initialize the move_group api
		moveit_commander.roscpp_initialize(sys.argv)
		rospy.init_node('moveit_demo',anonymous=True)
		#scene=PlanningSceneInterface()
		#self.scene_pub=rospy.Publisher('planning_scene',PlanningScene)
		#self.colors=dict()
		arm=MoveGroupCommander('arm')
		
		end_effector_link=arm.get_end_effector_link()
		reference_frame='base_link'
		arm.set_pose_reference_frame(reference_frame)
		arm.allow_replanning(True)
		arm.set_goal_position_tolerance(0.01)
		arm.set_goal_orientation_tolerance(0.01)
		arm.set_planning_time(5)
		
		'''
		l_tool_size=[0.02,0.02,0.1]
		p=PoseStamped()
		p.header.frame_id=end_effector_link
		p.pose.position.x=-0.0
		p.pose.position.y=0.03
		p.pose.position.z=0.0
		p.pose.orientation.w=1
		scene.attach_box(end_effector_link,'l_tool',p,l_tool_size) 
		
		r_tool_size=[0.02,0.02,0.1]
		p1=PoseStamped()
		p1.header.frame_id=end_effector_link
		p1.pose.position.x=-0.0
		p1.pose.position.y=-0.03
		p1.pose.position.z=0.0
		p1.pose.orientation.w=1
		scene.attach_box(end_effector_link,'r_tool',p1,r_tool_size) 
		'''
		'''
		table_id='table'
		box1_id='box1'
		box2_id='box2'
		tool_id='tool'
		
		scene.remove_world_object(box1_id)
		scene.remove_world_object(box2_id)
		scene.remove_world_object(table_id)
		scene.remove_attached_object(end_effector_link,tool_id)
		rospy.sleep(2)
		
		
		table_ground=0.36
		table_size=[0.5,0.7,0.01]
		box1_size=[0.1,0.05,0.03]
		box2_size=[0.05,0.05,0.1]
		tool_size=[0.2,0.02,0.02]

		table_pose=PoseStamped()
		table_pose.header.frame_id=reference_frame
		table_pose.pose.position.x=0.8
		table_pose.pose.position.y=0.0
		table_pose.pose.position.z=table_ground+table_size[2]/2.0
		table_pose.pose.orientation.w=1.0
		scene.add_box(table_id,table_pose,table_size)
		
		box1_pose=PoseStamped()
		box1_pose.header.frame_id=reference_frame
		box1_pose.pose.position.x=0.6
		box1_pose.pose.position.y=-0.2
		box1_pose.pose.position.z=table_ground+table_size[2]+box1_size[2]/2.0
		box1_pose.pose.orientation.w=1.0
		scene.add_box(box1_id,box1_pose,box1_size)

		box2_pose=PoseStamped()
		box2_pose.header.frame_id=reference_frame
		box2_pose.pose.position.x=0.6
		box2_pose.pose.position.y=0.0
		box2_pose.pose.position.z=table_ground+table_size[2]+box2_size[2]/2.0
		box2_pose.pose.orientation.w=1.0
		scene.add_box(box2_id,box2_pose,box2_size)	
		
		p=PoseStamped()
		p.header.frame_id=end_effector_link
		p.pose.position.x=-0.06
		p.pose.position.y=0.0
		p.pose.position.z=0.0
		p.pose.orientation.w=1
		scene.attach_box(end_effector_link,'tool',p,tool_size) 
		
		'''
		

		arm.set_named_target("initial_arm1")
		arm.go()
		rospy.sleep(5)
		
		target_pose=PoseStamped()
		target_pose.header.frame_id='base_footprint'
		target_pose.header.stamp=rospy.Time.now()
		target_pose.pose.position.x=0.4
		target_pose.pose.position.y=-0.09
		#target_pose.pose.position.z=table_pose.pose.position.z+table_size[2]+0.15
		target_pose.pose.position.z=0.7
		target_pose.pose.orientation.x=0
		target_pose.pose.orientation.y=0
		target_pose.pose.orientation.z=0
		target_pose.pose.orientation.w=1
		
		
		arm.set_start_state_to_current_state()
		
		arm.set_pose_target(target_pose,end_effector_link)
		#arm.go()
		traj=arm.plan()
		arm.execute(traj)
		rospy.sleep(5)
		arm.shift_pose_target(1,-0.1,end_effector_link)
		arm.go()
		
		arm.shift_pose_target(3,-1.57,end_effector_link)
		arm.go()
		rospy.sleep(5)
		
		saved_target_pose=arm.get_current_pose(end_effector_link)
		
		arm.set_named_target("initial_arm2")
		arm.go()
		rospy.sleep(2)
		
		arm.set_pose_target(saved_target_pose,end_effector_link)
		arm.go()
		rospy.sleep(2)
		
		arm.set_named_target("initial_arm1")
		arm.go()
		rospy.sleep(2)

		#traj=arm.plan()
		#arm.execute(traj)
		#rospy.sleep(1)
		#positions=  [0.113, 0.548, 0.767, 0.505, 0, -0.168, -0.197]
		#arm.set_joint_value_target(positions)
		#arm.go()
		#rospy.sleep(1)
		#scene.remove_attached_object(end_effector_link,tool_id)
		moveit_commander.roscpp_shutdown()
		moveit_commander.os._exit(0)
	
		
if __name__=="__main__":
	try:
		MoveItDemo()
	except KeyboardInterrupt:
			raise
		

