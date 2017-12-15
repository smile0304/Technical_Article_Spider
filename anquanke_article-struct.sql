/*
Navicat MySQL Data Transfer

Source Server         : TT_ubuntu16.04
Source Server Version : 50720
Source Host           : 192.168.123.66:3306
Source Database       : ArticleSpider

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2017-12-15 20:56:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for anquanke_article
-- ----------------------------
DROP TABLE IF EXISTS `anquanke_article`;
CREATE TABLE `anquanke_article` (
  `id` int(32) NOT NULL,
  `url` varchar(255) COLLATE utf8_bin NOT NULL,
  `title` varchar(50) COLLATE utf8_bin NOT NULL,
  `create_time` date NOT NULL,
  `cover_local` varchar(255) COLLATE utf8_bin NOT NULL,
  `watch_num` int(32) DEFAULT '0',
  `tags` varchar(255) COLLATE utf8_bin NOT NULL,
  `author` varchar(255) COLLATE utf8_bin NOT NULL,
  `comment_num` int(32) DEFAULT '0',
  `content` longtext COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
