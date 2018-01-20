#!/usr/bin/python

import roslib; roslib.load_manifest('motoman_driver')
import rospy
import sensor_msgs.msg
import trajectory_msgs.msg
import copy
import rospy,sys

import moveit_commander
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import PlanningScene, ObjectColor
from geometry_msgs.msg import PoseStamped, Pose 

from moveit_msgs.msg import Grasp,GripperTranslation,MoveItErrorCodes
from tf.transformations import quaternion_from_euler


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
		moveit_commander.roscpp_initialize(sys.argv)
		rospy.init_node('moveit_demo')
		scene=PlanningSceneInterface()
		self.scene_pub=rospy.Publisher('planning_scene',PlanningScene)
		self.colors=dict()
		rospy.sleep(1)
		arm=MoveGroupCommander('arm')
		end_effector_link=arm.get_end_effector_link()
		arm.set_goal_position_tolerance(0.008)
		arm.set_goal_orientation_tolerance(0.04)
		arm.allow_replanning(True)
		
		reference_frame='base_link'
		arm.set_pose_reference_frame(reference_frame)
		arm.set_planning_time(5)
		joint_state=[-2.419833894224669, 0.06734230828523968, -0.5274768816844496, 2.0819618074484882, -0.4270016439669033, -0.47903255506397024, -2.711311334870862]

		
		
		#scene planning
		table_id='table'
		#cylinder_id='cylinder'
		#box1_id='box1'
		box2_id='box2'
		target_id='target_object'
		#scene.remove_world_object(box1_id)
		scene.remove_world_object(box2_id)
		scene.remove_world_object(table_id)
		scene.remove_world_object(target_id)
		
		rospy.sleep(2)

		table_ground=0.5
		table_size=[0.5,1,0.01]
		#box1_size=[0.1,0.05,0.03]
		box2_size=[0.05,0.05,0.16]
		r_tool_size=[0.03,0.01,0.06]
		l_tool_size=[0.03,0.01,0.06]
		target_size=[0.05,0.05,0.16]
		

		table_pose=PoseStamped()
		table_pose.header.frame_id=reference_frame
		table_pose.pose.position.x=0.75
		table_pose.pose.position.y=0.0
		table_pose.pose.position.z=table_ground+table_size[2]/2.0
		table_pose.pose.orientation.w=1.0
		scene.add_box(table_id,table_pose,table_size)
		
		'''
		box1_pose=PoseStamped()
		box1_pose.header.frame_id=reference_frame
		box1_pose.pose.position.x=0.7
		box1_pose.pose.position.y=-0.2
		box1_pose.pose.position.z=table_ground+table_size[2]+box1_size[2]/2.0
		box1_pose.pose.orientation.w=1.0
		scene.add_box(box1_id,box1_pose,box1_size)
		'''
		
		box2_pose=PoseStamped()
		box2_pose.header.frame_id=reference_frame
		box2_pose.pose.position.x=0.6
		box2_pose.pose.position.y=-0.05
		box2_pose.pose.position.z=table_ground+table_size[2]+box2_size[2]/2.0
		box2_pose.pose.orientation.w=1.0
		scene.add_box(box2_id,box2_pose,box2_size)	
		
		target_pose=PoseStamped()
		target_pose.header.frame_id=reference_frame
		target_pose.pose.position.x=0.6
		target_pose.pose.position.y=0.05
		target_pose.pose.position.z=table_ground+table_size[2]+target_size[2]/2.0
		target_pose.pose.orientation.x=0
		target_pose.pose.orientation.y=0
		target_pose.pose.orientation.z=0
		target_pose.pose.orientation.w=1
		scene.add_box(target_id,target_pose,target_size)	
		
		#left gripper
		l_p=PoseStamped()
		l_p.header.frame_id=end_effector_link
		l_p.pose.position.x=0.00
		l_p.pose.position.y=0.04
		l_p.pose.position.z=0.04
		l_p.pose.orientation.w=1
		scene.attach_box(end_effector_link,'l_tool',l_p,l_tool_size)	
		
		#right gripper
		r_p=PoseStamped()
		r_p.header.frame_id=end_effector_link
		r_p.pose.position.x=0.00
		r_p.pose.position.y=-0.04
		r_p.pose.position.z=0.04
		r_p.pose.orientation.w=1
		scene.attach_box(end_effector_link,'r_tool',r_p,r_tool_size)	
		
		#grasp
		g_p=PoseStamped()
		g_p.header.frame_id=end_effector_link
		g_p.pose.position.x=0.00
		g_p.pose.position.y=-0.00
		g_p.pose.position.z=0.025
		g_p.pose.orientation.w=0.707
		g_p.pose.orientation.x=0
		g_p.pose.orientation.y=-0.707
		g_p.pose.orientation.z=0
		
		#set color
		self.setColor(table_id,0.8,0,0,1.0)
		#self.setColor(box1_id,0.8,0.4,0,1.0)
		self.setColor(box2_id,0.8,0.4,0,1.0)
		self.setColor('r_tool',0.8,0,0)
		self.setColor('l_tool',0.8,0,0)
		self.setColor('target_object',0,1,0)
		self.sendColors()
		
		#motion planning
		arm.set_named_target("initial_arm1")
		arm.go()
		rospy.sleep(2)
		
		grasp_pose=target_pose
		grasp_pose.pose.position.x-=0.13
		#grasp_pose.pose.position.z=
		grasp_pose.pose.orientation.x=0
		grasp_pose.pose.orientation.y=0.707
		grasp_pose.pose.orientation.z=0
		grasp_pose.pose.orientation.w=0.707
		
		arm.set_start_state_to_current_state()
		arm.set_pose_target(grasp_pose,end_effector_link)
		#arm.set_joint_value_target(joint_state)
		traj=arm.plan()
		arm.execute(traj)
		rospy.sleep(2)
		print arm.get_current_joint_values()
		#arm.shift_pose_target(4,1.57,end_effector_link)
		#arm.go()
		#rospy.sleep(2)
		arm.shift_pose_target(0,0.11,end_effector_link)
		arm.go()
		rospy.sleep(2)
		print arm.get_current_joint_values()
		saved_target_pose=arm.get_current_pose(end_effector_link)
		#arm.set_named_target("initial_arm2")
		
		#grasp
		scene.attach_box(end_effector_link,target_id,g_p,target_size)	
		rospy.sleep(2)
		
		
		#grasping is over , from now is placing 
		arm.shift_pose_target(2,0.18,end_effector_link)
		arm.go()
		rospy.sleep(2)
		
		arm.shift_pose_target(1,-0.2,end_effector_link)
		arm.go()
		rospy.sleep(2)
		print arm.get_current_joint_values()
		arm.shift_pose_target(2,-0.18,end_effector_link)
		arm.go()
		rospy.sleep(2)
		scene.remove_attached_object(end_effector_link,target_id)
		rospy.sleep(2)
		#arm.set_pose_target(saved_target_pose,end_effector_link)
		#arm.go()
		#rospy.sleep(2)
		
		arm.set_named_target("initial_arm1")
		arm.go()
		rospy.sleep(2)

		#remove and shut down
		scene.remove_attached_object(end_effector_link,'l_tool')
		scene.remove_attached_object(end_effector_link,'r_tool')
		moveit_commander.roscpp_shutdown()
		moveit_commander.os._exit(0)
		
		
		
		
		
		
if __name__=="__main__":
	try:
		MoveItDemo()
	except KeyboardInterrupt:
			raise
		

