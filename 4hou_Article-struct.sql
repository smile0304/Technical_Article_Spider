/*
Navicat MySQL Data Transfer

Source Server         : TT_ubuntu16.04
Source Server Version : 50720
Source Host           : 192.168.250.66:3306
Source Database       : ArticleSpider

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2017-12-05 15:03:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 4hou_Article
-- ----------------------------
DROP TABLE IF EXISTS `4hou_Article`;
CREATE TABLE `4hou_Article` (
  `image_local` varchar(255) COLLATE utf8_bin NOT NULL,
  `image_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `title` varchar(200) COLLATE utf8_bin NOT NULL,
  `url_id` varchar(32) COLLATE utf8_bin NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(100) COLLATE utf8_bin NOT NULL,
  `author` varchar(200) COLLATE utf8_bin NOT NULL,
  `tags` varchar(50) COLLATE utf8_bin NOT NULL,
  `watch_num` int(10) DEFAULT '0' COMMENT '0',
  `comment_num` int(10) DEFAULT '0',
  `praise_nums` int(10) DEFAULT '0',
  `content` longtext COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`url_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=DYNAMIC;
