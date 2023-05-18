/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50620
Source Host           : localhost:3306
Source Database       : score_db

Target Server Type    : MYSQL
Target Server Version : 50620
File Encoding         : 65001

Date: 2019-09-20 00:27:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_admin`
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin` (
  `username` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for `t_attendance`
-- ----------------------------
DROP TABLE IF EXISTS `t_attendance`;
CREATE TABLE `t_attendance` (
  `attendanceId` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录编号',
  `studentObj` varchar(20) NOT NULL COMMENT '学生',
  `courseObj` varchar(20) NOT NULL COMMENT '课程',
  `timeInfoObj` int(11) NOT NULL COMMENT '时间',
  `attendanceStateObj` varchar(20) NOT NULL COMMENT '状态',
  PRIMARY KEY (`attendanceId`),
  KEY `studentObj` (`studentObj`),
  KEY `courseObj` (`courseObj`),
  KEY `timeInfoObj` (`timeInfoObj`),
  KEY `attendanceStateObj` (`attendanceStateObj`),
  CONSTRAINT `t_attendance_ibfk_1` FOREIGN KEY (`studentObj`) REFERENCES `t_student` (`studentNumber`),
  CONSTRAINT `t_attendance_ibfk_2` FOREIGN KEY (`courseObj`) REFERENCES `t_course` (`courseNo`),
  CONSTRAINT `t_attendance_ibfk_3` FOREIGN KEY (`timeInfoObj`) REFERENCES `t_timeinfo` (`timeInfoId`),
  CONSTRAINT `t_attendance_ibfk_4` FOREIGN KEY (`attendanceStateObj`) REFERENCES `t_attendancestate` (`stateId`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_attendance
-- ----------------------------
INSERT INTO `t_attendance` VALUES ('1', 'STU001', 'KC001', '1', '1');
INSERT INTO `t_attendance` VALUES ('2', 'STU001', 'KC002', '1', '1');
INSERT INTO `t_attendance` VALUES ('3', 'STU002', 'KC001', '1', '1');
INSERT INTO `t_attendance` VALUES ('4', 'STU002', 'KC002', '1', '2');
INSERT INTO `t_attendance` VALUES ('5', 'STU001', 'KC001', '2', '3');
INSERT INTO `t_attendance` VALUES ('6', 'STU001', 'KC001', '3', '1');

-- ----------------------------
-- Table structure for `t_attendancestate`
-- ----------------------------
DROP TABLE IF EXISTS `t_attendancestate`;
CREATE TABLE `t_attendancestate` (
  `stateId` varchar(20) NOT NULL COMMENT 'stateId',
  `stateName` varchar(20) NOT NULL COMMENT '状态名称',
  PRIMARY KEY (`stateId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_attendancestate
-- ----------------------------
INSERT INTO `t_attendancestate` VALUES ('1', '已到');
INSERT INTO `t_attendancestate` VALUES ('2', '缺席');
INSERT INTO `t_attendancestate` VALUES ('3', '请假');

-- ----------------------------
-- Table structure for `t_classinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_classinfo`;
CREATE TABLE `t_classinfo` (
  `classNo` varchar(20) NOT NULL COMMENT 'classNo',
  `className` varchar(20) NOT NULL COMMENT '班级名称',
  `banzhuren` varchar(20) DEFAULT NULL COMMENT '班主任姓名',
  `beginDate` varchar(20) DEFAULT NULL COMMENT '成立日期',
  PRIMARY KEY (`classNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_classinfo
-- ----------------------------
INSERT INTO `t_classinfo` VALUES ('BJ001', '计算机1班', '王涛', '2019-06-12');
INSERT INTO `t_classinfo` VALUES ('BJ002', '计算机2班', '黄小兵', '2019-09-11');

-- ----------------------------
-- Table structure for `t_course`
-- ----------------------------
DROP TABLE IF EXISTS `t_course`;
CREATE TABLE `t_course` (
  `courseNo` varchar(20) NOT NULL COMMENT 'courseNo',
  `courseName` varchar(20) NOT NULL COMMENT '课程名称',
  `teacherName` varchar(20) DEFAULT NULL COMMENT '任课教师',
  `courseCount` int(11) NOT NULL COMMENT '总课时',
  `courseScore` float NOT NULL COMMENT '总学分',
  PRIMARY KEY (`courseNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_course
-- ----------------------------
INSERT INTO `t_course` VALUES ('KC001', 'python网络编程', '李晓彤', '45', '3.5');
INSERT INTO `t_course` VALUES ('KC002', 'PHP网站开发', '邓自强', '35', '3');

-- ----------------------------
-- Table structure for `t_scoreinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_scoreinfo`;
CREATE TABLE `t_scoreinfo` (
  `scoreId` int(11) NOT NULL AUTO_INCREMENT COMMENT '成绩编号',
  `studentNumber` varchar(20) NOT NULL COMMENT '学生姓名',
  `courseNo` varchar(20) NOT NULL COMMENT '课程名称',
  `termId` int(11) NOT NULL COMMENT '所在学期',
  `score` float NOT NULL COMMENT '成绩得分',
  PRIMARY KEY (`scoreId`),
  KEY `studentNumber` (`studentNumber`),
  KEY `courseNo` (`courseNo`),
  KEY `termId` (`termId`),
  CONSTRAINT `t_scoreinfo_ibfk_1` FOREIGN KEY (`studentNumber`) REFERENCES `t_student` (`studentNumber`),
  CONSTRAINT `t_scoreinfo_ibfk_2` FOREIGN KEY (`courseNo`) REFERENCES `t_course` (`courseNo`),
  CONSTRAINT `t_scoreinfo_ibfk_3` FOREIGN KEY (`termId`) REFERENCES `t_terminfo` (`termId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_scoreinfo
-- ----------------------------
INSERT INTO `t_scoreinfo` VALUES ('1', 'STU001', 'KC001', '1', '82.5');
INSERT INTO `t_scoreinfo` VALUES ('2', 'STU001', 'KC002', '1', '88');
INSERT INTO `t_scoreinfo` VALUES ('3', 'STU002', 'KC001', '1', '92');

-- ----------------------------
-- Table structure for `t_student`
-- ----------------------------
DROP TABLE IF EXISTS `t_student`;
CREATE TABLE `t_student` (
  `studentNumber` varchar(20) NOT NULL COMMENT 'studentNumber',
  `studentName` varchar(20) NOT NULL COMMENT '姓名',
  `sex` varchar(2) NOT NULL COMMENT '性别',
  `classInfoId` varchar(20) NOT NULL COMMENT '所在班级',
  `birthday` varchar(20) DEFAULT NULL COMMENT '出生日期',
  `zzmm` varchar(10) DEFAULT NULL COMMENT '政治面貌',
  `telephone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `address` varchar(50) DEFAULT NULL COMMENT '家庭地址',
  `photoUrl` varchar(60) NOT NULL COMMENT '学生照片',
  PRIMARY KEY (`studentNumber`),
  KEY `classInfoId` (`classInfoId`),
  CONSTRAINT `t_student_ibfk_1` FOREIGN KEY (`classInfoId`) REFERENCES `t_classinfo` (`classNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_student
-- ----------------------------
INSERT INTO `t_student` VALUES ('STU001', '李晓芳', '女', 'BJ001', '2019-09-10', '团员', '13080893412', '四川成都红星路', 'img/8.jpg');
INSERT INTO `t_student` VALUES ('STU002', '王霞', '女', 'BJ002', '2019-09-03', '党员', '13908312423', '四川南充冰江路', 'img/9.jpg');

-- ----------------------------
-- Table structure for `t_terminfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_terminfo`;
CREATE TABLE `t_terminfo` (
  `termId` int(11) NOT NULL AUTO_INCREMENT COMMENT '学期编号',
  `termName` varchar(20) DEFAULT NULL COMMENT '学期名称',
  PRIMARY KEY (`termId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_terminfo
-- ----------------------------
INSERT INTO `t_terminfo` VALUES ('1', '2019-2020上学期');
INSERT INTO `t_terminfo` VALUES ('2', '2019-2020下学期');

-- ----------------------------
-- Table structure for `t_timeinfo`
-- ----------------------------
DROP TABLE IF EXISTS `t_timeinfo`;
CREATE TABLE `t_timeinfo` (
  `timeInfoId` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录编号',
  `timeInfoName` varchar(20) NOT NULL COMMENT '学时名称',
  PRIMARY KEY (`timeInfoId`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_timeinfo
-- ----------------------------
INSERT INTO `t_timeinfo` VALUES ('1', '第1学时');
INSERT INTO `t_timeinfo` VALUES ('2', '第2学时');
INSERT INTO `t_timeinfo` VALUES ('3', '第3学时');
INSERT INTO `t_timeinfo` VALUES ('4', '第4学时');
INSERT INTO `t_timeinfo` VALUES ('5', '第5学时');
INSERT INTO `t_timeinfo` VALUES ('6', '第6学时');
INSERT INTO `t_timeinfo` VALUES ('7', '第7学时');
INSERT INTO `t_timeinfo` VALUES ('8', '第8学时');
INSERT INTO `t_timeinfo` VALUES ('9', '第9学时');
INSERT INTO `t_timeinfo` VALUES ('10', '第10学时');
INSERT INTO `t_timeinfo` VALUES ('11', '第11学时');
INSERT INTO `t_timeinfo` VALUES ('12', '第12学时');
INSERT INTO `t_timeinfo` VALUES ('13', '第13学时');
INSERT INTO `t_timeinfo` VALUES ('14', '第14学时');
INSERT INTO `t_timeinfo` VALUES ('15', '第15学时');
INSERT INTO `t_timeinfo` VALUES ('16', '第16学时');
INSERT INTO `t_timeinfo` VALUES ('17', '第17学时');
INSERT INTO `t_timeinfo` VALUES ('18', '第18学时');
INSERT INTO `t_timeinfo` VALUES ('19', '第19学时');
INSERT INTO `t_timeinfo` VALUES ('20', '第20学时');
